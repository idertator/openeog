from PySide6 import QtCore, QtWidgets

from bsp.gui.screens import ScreensManager
from bsp.settings import config


class FinishingPage(QtWidgets.QWizardPage):
    def __init__(
        self,
        screens: ScreensManager,
        parent: QtWidgets.QWidget = None,
    ):
        super().__init__(parent=parent)

        self.setTitle("Finalizando la Configuración")
        self.setFinalPage(True)

        self._screens = screens

        device_type = self.device_type
        if device_type not in config.DEVICE_TYPES:
            device_type = config.DEVICE_TYPES[-1]
            self.device_type = device_type

        self._device_type = QtWidgets.QComboBox()
        self._device_type.addItems(config.DEVICE_TYPES)
        self._device_type.setCurrentText(device_type)
        self._device_type.currentTextChanged.connect(self.on_device_type_changed)

        self._device_address = QtWidgets.QLineEdit()
        self._device_address.setText(config.default_device_address)
        self._device_address.textChanged.connect(self.on_device_address_changed)

        stimuli_monitor = self.stimuli_monitor
        if stimuli_monitor not in screens.screen_list:
            stimuli_monitor = screens.screen_list[-1]
            self.stimuli_monitor = stimuli_monitor

        self._stimuli_monitor = QtWidgets.QComboBox()
        self._stimuli_monitor.addItems(screens.screen_list)
        self._stimuli_monitor.setCurrentText(stimuli_monitor)
        self._stimuli_monitor.currentTextChanged.connect(
            self.on_stimuli_monitor_changed
        )

        layout = QtWidgets.QFormLayout()
        layout.addRow("Tipo de Dispositivo", self._device_type)
        layout.addRow("Dispositivo", self._device_address)
        layout.addRow("Pantalla de Estímulo", self._stimuli_monitor)

        self.setLayout(layout)

    @property
    def device_type(self) -> str:
        settings = QtCore.QSettings()
        return settings.value("device_type", "BiosignalsPlux")

    @device_type.setter
    def device_type(self, value: str):
        settings = QtCore.QSettings()
        settings.setValue("device_type", value)

    @property
    def resolution(self) -> int:
        if self.device_type == "Bitalino":
            return 10
        return 16

    @property
    def device_address(self) -> str:
        settings = QtCore.QSettings()
        return settings.value("device_address", "/dev/rfcomm0")

    @device_address.setter
    def device_address(self, value: str):
        settings = QtCore.QSettings()
        settings.setValue("device_address", value)

    @property
    def stimuli_monitor(self) -> str:
        settings = QtCore.QSettings()
        return settings.value("stimuli_monitor", self._screens.screen_list[-1])

    @stimuli_monitor.setter
    def stimuli_monitor(self, value: str):
        settings = QtCore.QSettings()
        settings.setValue("stimuli_monitor", value)

    @QtCore.Slot()
    def on_device_address_changed(self):
        self.device_address = self._device_address.text()

    @QtCore.Slot()
    def on_stimuli_monitor_changed(self, screen: str):
        self.stimuli_monitor = screen

    @QtCore.Slot()
    def on_device_type_changed(self, device_type: str):
        self.device_type = device_type
