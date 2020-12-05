# Copyright (c) 2019 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.
from time import time
from typing import List, Optional, cast

from PyQt5.QtCore import QObject, QUrl, pyqtProperty, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QDesktopServices

from UM import i18nCatalog
from UM.Backend.Backend import BackendState
from UM.FileHandler.FileHandler import FileHandler
from UM.Logger import Logger
from UM.Scene.SceneNode import SceneNode
from UM.Version import Version
from cura.CuraApplication import CuraApplication
from cura.PrinterOutput.NetworkedPrinterOutputDevice import AuthState
from cura.PrinterOutput.PrinterOutputDevice import ConnectionType

from .CloudApiClient import CloudApiClient
from ..ExportFileJob import ExportFileJob
from ..UltimakerNetworkedPrinterOutputDevice import UltimakerNetworkedPrinterOutputDevice
from ..Messages.PrintJobUploadBlockedMessage import PrintJobUploadBlockedMessage
from ..Messages.PrintJobUploadErrorMessage import PrintJobUploadErrorMessage
from ..Messages.PrintJobUploadSuccessMessage import PrintJobUploadSuccessMessage
from ..Models.Http.CloudClusterResponse import CloudClusterResponse
from ..Models.Http.CloudClusterStatus import CloudClusterStatus
from ..Models.Http.CloudPrintJobUploadRequest import CloudPrintJobUploadRequest
from ..Models.Http.CloudPrintResponse import CloudPrintResponse
from ..Models.Http.CloudPrintJobResponse import CloudPrintJobResponse
from ..Models.Http.ClusterPrinterStatus import ClusterPrinterStatus
from ..Models.Http.ClusterPrintJobStatus import ClusterPrintJobStatus


I18N_CATALOG = i18nCatalog("cura")


##  The cloud output device is a network output device that works remotely but has limited functionality.
#   Currently it only supports viewing the printer and print job status and adding a new job to the queue.
#   As such, those methods have been implemented here.
#   Note that this device represents a single remote cluster, not a list of multiple clusters.
class CloudOutputDevice(UltimakerNetworkedPrinterOutputDevice):

    # The interval with which the remote cluster is checked.
    # We can do this relatively often as this API call is quite fast.
    CHECK_CLUSTER_INTERVAL = 10.0  # seconds

    # Override the network response timeout in seconds after which we consider the device offline.
    # For cloud this needs to be higher because the interval at which we check the status is higher as well.
    NETWORK_RESPONSE_CONSIDER_OFFLINE = 15.0  # seconds

    # The minimum version of firmware that support print job actions over cloud.
    PRINT_JOB_ACTIONS_MIN_VERSION = Version("5.3.0")

    # Notify can only use signals that are defined by the class that they are in, not inherited ones.
    # Therefore we create a private signal used to trigger the printersChanged signal.
    _cloudClusterPrintersChanged = pyqtSignal()

    ## Creates a new cloud output device
    #  \param api_client: The client that will run the API calls
    #  \param cluster: The device response received from the cloud API.
    #  \param parent: The optional parent of this output device.
    def __init__(self, api_client: CloudApiClient, cluster: CloudClusterResponse, parent: QObject = None) -> None:

        # The following properties are expected on each networked output device.
        # Because the cloud connection does not off all of these, we manually construct this version here.
        # An example of why this is needed is the selection of the compatible file type when exporting the tool path.
        properties = {
            b"address": cluster.host_internal_ip.encode() if cluster.host_internal_ip else b"",
            b"name": cluster.friendly_name.encode() if cluster.friendly_name else b"",
            b"firmware_version": cluster.host_version.encode() if cluster.host_version else b"",
            b"printer_type": cluster.printer_type.encode() if cluster.printer_type else b"",
            b"cluster_size": b"1"  # cloud devices are always clusters of at least one
        }

        super().__init__(
            device_id=cluster.cluster_id,
            address="",
            connection_type=ConnectionType.CloudConnection,
            properties=properties,
            parent=parent
        )

        self._api = api_client
        self._account = api_client.account
        self._cluster = cluster
        self.setAuthenticationState(AuthState.NotAuthenticated)
        self._setInterfaceElements()

        # Trigger the printersChanged signal when the private signal is triggered.
        self.printersChanged.connect(self._cloudClusterPrintersChanged)

        # Keep server string of the last generated time to avoid updating models more than once for the same response
        self._received_printers = None  # type: Optional[List[ClusterPrinterStatus]]
        self._received_print_jobs = None  # type: Optional[List[ClusterPrintJobStatus]]

        # Reference to the uploaded print job / mesh
        # We do this to prevent re-uploading the same file multiple times.
        self._tool_path = None  # type: Optional[bytes]
        self._uploaded_print_job = None  # type: Optional[CloudPrintJobResponse]

    ## Connects this device.
    def connect(self) -> None:
        if self.isConnected():
            return
        super().connect()
        Logger.log("i", "Connected to cluster %s", self.key)
        CuraApplication.getInstance().getBackend().backendStateChange.connect(self._onBackendStateChange)
        self._update()

    ## Disconnects the device
    def disconnect(self) -> None:
        if not self.isConnected():
            return
        super().disconnect()
        Logger.log("i", "Disconnected from cluster %s", self.key)
        CuraApplication.getInstance().getBackend().backendStateChange.disconnect(self._onBackendStateChange)

    ## Resets the print job that was uploaded to force a new upload, runs whenever the user re-slices.
    def _onBackendStateChange(self, _: BackendState) -> None:
        self._tool_path = None
        self._uploaded_print_job = None

    ## Checks whether the given network key is found in the cloud's host name
    def matchesNetworkKey(self, network_key: str) -> bool:
        # Typically, a network key looks like "ultimakersystem-aabbccdd0011._ultimaker._tcp.local."
        # the host name should then be "ultimakersystem-aabbccdd0011"
        if network_key.startswith(str(self.clusterData.host_name or "")):
            return True
        # However, for manually added printers, the local IP address is used in lieu of a proper
        # network key, so check for that as well. It is in the format "manual:10.1.10.1".
        if network_key.endswith(str(self.clusterData.host_internal_ip or "")):
            return True
        return False

    ## Set all the interface elements and texts for this output device.
    def _setInterfaceElements(self) -> None:
        self.setPriority(2)  # Make sure we end up below the local networking and above 'save to file'.
        self.setShortDescription(I18N_CATALOG.i18nc("@action:button", "Print via Cloud"))
        self.setDescription(I18N_CATALOG.i18nc("@properties:tooltip", "Print via Cloud"))
        self.setConnectionText(I18N_CATALOG.i18nc("@info:status", "Connected via Cloud"))

    ## Called when the network data should be updated.
    def _update(self) -> None:
        super()._update()
        if time() - self._time_of_last_request < self.CHECK_CLUSTER_INTERVAL:
            return  # avoid calling the cloud too often
        self._time_of_last_request = time()
        if self._account.isLoggedIn:
            self.setAuthenticationState(AuthState.Authenticated)
            self._last_request_time = time()
            self._api.getClusterStatus(self.key, self._onStatusCallFinished)
        else:
            self.setAuthenticationState(AuthState.NotAuthenticated)

    ## Method called when HTTP request to status endpoint is finished.
    #  Contains both printers and print jobs statuses in a single response.
    def _onStatusCallFinished(self, status: CloudClusterStatus) -> None:
        self._responseReceived()
        if status.printers != self._received_printers:
            self._received_printers = status.printers
            self._updatePrinters(status.printers)
        if status.print_jobs != self._received_print_jobs:
            self._received_print_jobs = status.print_jobs
            self._updatePrintJobs(status.print_jobs)

    ##  Called when Cura requests an output device to receive a (G-code) file.
    def requestWrite(self, nodes: List[SceneNode], file_name: Optional[str] = None, limit_mimetypes: bool = False,
                     file_handler: Optional[FileHandler] = None, filter_by_machine: bool = False, **kwargs) -> None:

        # Show an error message if we're already sending a job.
        if self._progress.visible:
            PrintJobUploadBlockedMessage().show()
            return

        # Indicate we have started sending a job.
        self.writeStarted.emit(self)

        # The mesh didn't change, let's not upload it to the cloud again.
        # Note that self.writeFinished is called in _onPrintUploadCompleted as well.
        if self._uploaded_print_job:
            self._api.requestPrint(self.key, self._uploaded_print_job.job_id, self._onPrintUploadCompleted)
            return

        # Export the scene to the correct file type.
        job = ExportFileJob(file_handler=file_handler, nodes=nodes, firmware_version=self.firmwareVersion)
        job.finished.connect(self._onPrintJobCreated)
        job.start()

    ## Handler for when the print job was created locally.
    #  It can now be sent over the cloud.
    def _onPrintJobCreated(self, job: ExportFileJob) -> None:
        output = job.getOutput()
        self._tool_path = output  # store the tool path to prevent re-uploading when printing the same file again
        request = CloudPrintJobUploadRequest(
            job_name=job.getFileName(),
            file_size=len(output),
            content_type=job.getMimeType(),
        )
        self._api.requestUpload(request, self._uploadPrintJob)

    ## Uploads the mesh when the print job was registered with the cloud API.
    #  \param job_response: The response received from the cloud API.
    def _uploadPrintJob(self, job_response: CloudPrintJobResponse) -> None:
        if not self._tool_path:
            return self._onUploadError()
        self._progress.show()
        self._uploaded_print_job = job_response  # store the last uploaded job to prevent re-upload of the same file
        self._api.uploadToolPath(job_response, self._tool_path, self._onPrintJobUploaded, self._progress.update,
                                 self._onUploadError)

    ## Requests the print to be sent to the printer when we finished uploading the mesh.
    def _onPrintJobUploaded(self) -> None:
        self._progress.update(100)
        print_job = cast(CloudPrintJobResponse, self._uploaded_print_job)
        self._api.requestPrint(self.key, print_job.job_id, self._onPrintUploadCompleted)

    ## Shows a message when the upload has succeeded
    #  \param response: The response from the cloud API.
    def _onPrintUploadCompleted(self, response: CloudPrintResponse) -> None:
        self._progress.hide()
        PrintJobUploadSuccessMessage().show()
        self.writeFinished.emit()

    ## Displays the given message if uploading the mesh has failed
    #  \param message: The message to display.
    def _onUploadError(self, message: str = None) -> None:
        self._progress.hide()
        self._uploaded_print_job = None
        PrintJobUploadErrorMessage(message).show()
        self.writeError.emit()

    ##  Whether the printer that this output device represents supports print job actions via the cloud.
    @pyqtProperty(bool, notify=_cloudClusterPrintersChanged)
    def supportsPrintJobActions(self) -> bool:
        if not self._printers:
            return False
        version_number = self.printers[0].firmwareVersion.split(".")
        firmware_version = Version([version_number[0], version_number[1], version_number[2]])
        return firmware_version >= self.PRINT_JOB_ACTIONS_MIN_VERSION

    ##  Set the remote print job state.
    def setJobState(self, print_job_uuid: str, state: str) -> None:
        self._api.doPrintJobAction(self._cluster.cluster_id, print_job_uuid, state)

    @pyqtSlot(str, name="sendJobToTop")
    def sendJobToTop(self, print_job_uuid: str) -> None:
        self._api.doPrintJobAction(self._cluster.cluster_id, print_job_uuid, "move",
                                   {"list": "queued", "to_position": 0})

    @pyqtSlot(str, name="deleteJobFromQueue")
    def deleteJobFromQueue(self, print_job_uuid: str) -> None:
        self._api.doPrintJobAction(self._cluster.cluster_id, print_job_uuid, "remove")

    @pyqtSlot(str, name="forceSendJob")
    def forceSendJob(self, print_job_uuid: str) -> None:
        self._api.doPrintJobAction(self._cluster.cluster_id, print_job_uuid, "force")

    @pyqtSlot(name="openPrintJobControlPanel")
    def openPrintJobControlPanel(self) -> None:
        QDesktopServices.openUrl(QUrl(self.clusterCloudUrl))

    @pyqtSlot(name="openPrinterControlPanel")
    def openPrinterControlPanel(self) -> None:
        QDesktopServices.openUrl(QUrl(self.clusterCloudUrl))

    ## Gets the cluster response from which this device was created.
    @property
    def clusterData(self) -> CloudClusterResponse:
        return self._cluster

    ## Updates the cluster data from the cloud.
    @clusterData.setter
    def clusterData(self, value: CloudClusterResponse) -> None:
        self._cluster = value

    ## Gets the URL on which to monitor the cluster via the cloud.
    @property
    def clusterCloudUrl(self) -> str:
        root_url_prefix = "-staging" if self._account.is_staging else ""
        return "https://mycloud{}.ultimaker.com/app/jobs/{}".format(root_url_prefix, self.clusterData.cluster_id)
