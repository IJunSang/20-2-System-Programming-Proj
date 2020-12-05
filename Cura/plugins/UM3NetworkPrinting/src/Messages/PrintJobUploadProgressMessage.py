# Copyright (c) 2019 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.
from UM import i18nCatalog
from UM.Message import Message


I18N_CATALOG = i18nCatalog("cura")


## Class responsible for showing a progress message while a mesh is being uploaded to the cloud.
class PrintJobUploadProgressMessage(Message):
    def __init__(self):
        super().__init__(
            title = I18N_CATALOG.i18nc("@info:status", "Sending Print Job"),
            text = I18N_CATALOG.i18nc("@info:status", "Uploading print job to printer."),
            progress = -1,
            lifetime = 0,
            dismissable = False,
            use_inactivity_timer = False
        )

    ## Shows the progress message.
    def show(self):
        self.setProgress(0)
        super().show()

    ## Updates the percentage of the uploaded.
    #  \param percentage: The percentage amount (0-100).
    def update(self, percentage: int) -> None:
        if not self._visible:
            super().show()
        self.setProgress(percentage)
