# Copyright (c) 2019 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.
from typing import Optional, cast

from PyQt5.QtCore import pyqtSlot, pyqtSignal, pyqtProperty, QObject

from UM import i18nCatalog
from cura.CuraApplication import CuraApplication
from cura.MachineAction import MachineAction

from .UM3OutputDevicePlugin import UM3OutputDevicePlugin
from .Network.LocalClusterOutputDevice import LocalClusterOutputDevice


I18N_CATALOG = i18nCatalog("cura")


## Machine action that allows to connect the active machine to a networked devices.
#  TODO: in the future this should be part of the new discovery workflow baked into Cura.
class UltimakerNetworkedPrinterAction(MachineAction):

    # Signal emitted when discovered devices have changed.
    discoveredDevicesChanged = pyqtSignal()

    def __init__(self) -> None:
        super().__init__("DiscoverUM3Action", I18N_CATALOG.i18nc("@action", "Connect via Network"))
        self._qml_url = "resources/qml/DiscoverUM3Action.qml"
        self._network_plugin = None  # type: Optional[UM3OutputDevicePlugin]

    ## Override the default value.
    def needsUserInteraction(self) -> bool:
        return False

    ## Start listening to network discovery events via the plugin.
    @pyqtSlot(name = "startDiscovery")
    def startDiscovery(self) -> None:
        self._networkPlugin.discoveredDevicesChanged.connect(self._onDeviceDiscoveryChanged)
        self.discoveredDevicesChanged.emit()  # trigger at least once to populate the list

    ## Reset the discovered devices.
    @pyqtSlot(name = "reset")
    def reset(self) -> None:
        self.discoveredDevicesChanged.emit()  # trigger to reset the list

    ## Reset the discovered devices.
    @pyqtSlot(name = "restartDiscovery")
    def restartDiscovery(self) -> None:
        self._networkPlugin.startDiscovery()
        self.discoveredDevicesChanged.emit()  # trigger to reset the list

    ## Remove a manually added device.
    @pyqtSlot(str, str, name = "removeManualDevice")
    def removeManualDevice(self, key: str, address: str) -> None:
        self._networkPlugin.removeManualDevice(key, address)

    ## Add a new manual device. Can replace an existing one by key.
    @pyqtSlot(str, str, name = "setManualDevice")
    def setManualDevice(self, key: str, address: str) -> None:
        if key != "":
            self._networkPlugin.removeManualDevice(key)
        if address != "":
            self._networkPlugin.addManualDevice(address)

    ## Get the devices discovered in the local network sorted by name.
    @pyqtProperty("QVariantList", notify = discoveredDevicesChanged)
    def foundDevices(self):
        discovered_devices = list(self._networkPlugin.getDiscoveredDevices().values())
        discovered_devices.sort(key = lambda d: d.name)
        return discovered_devices

    ## Connect a device selected in the list with the active machine.
    @pyqtSlot(QObject, name = "associateActiveMachineWithPrinterDevice")
    def associateActiveMachineWithPrinterDevice(self, device: LocalClusterOutputDevice) -> None:
        self._networkPlugin.associateActiveMachineWithPrinterDevice(device)

    ## Callback for when the list of discovered devices in the plugin was changed.
    def _onDeviceDiscoveryChanged(self) -> None:
        self.discoveredDevicesChanged.emit()

    ## Get the network manager from the plugin.
    @property
    def _networkPlugin(self) -> UM3OutputDevicePlugin:
        if not self._network_plugin:
            output_device_manager = CuraApplication.getInstance().getOutputDeviceManager()
            network_plugin = output_device_manager.getOutputDevicePlugin("UM3NetworkPrinting")
            self._network_plugin = cast(UM3OutputDevicePlugin, network_plugin)
        return self._network_plugin
