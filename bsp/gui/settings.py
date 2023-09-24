from PySide6.QtCore import QSettings, Slot
from PySide6.QtWidgets import QComboBox, QDialog, QFormLayout, QLineEdit, QWidget

from .screens import ScreensManager


class SettingsDialog(QDialog):
    def __init__(
        self,
        screens: ScreensManager,
        parent: QWidget = None,
    ):
        super().__init__(parent=parent)
        self.setWindowTitle("Configuración")

        self._screens = screens

        settings = QSettings()

        self._device_address = QLineEdit()
        self._device_address.setText(settings.value("device_address", "/dev/rfcomm0"))
        self._device_address.textChanged.connect(self.on_device_address_changed)

        stimuli_monitor = self.stimuli_monitor
        if stimuli_monitor not in screens.screen_list:
            stimuli_monitor = screens.screen_list[-1]
            self.stimuli_monitor = stimuli_monitor

        self._stimuli_monitor = QComboBox()
        self._stimuli_monitor.addItems(screens.screen_list)
        self._stimuli_monitor.setCurrentText(stimuli_monitor)
        self._stimuli_monitor.currentTextChanged.connect(
            self.on_stimuli_monitor_changed
        )

        layout = QFormLayout()
        layout.addRow("Dispositivo", self._device_address)
        layout.addRow("Pantalla de Estímulo", self._stimuli_monitor)

        self.setLayout(layout)

    @property
    def device_address(self) -> str:
        settings = QSettings()
        return settings.value("device_address", "/dev/rfcomm0")

    @device_address.setter
    def device_address(self, value: str):
        settings = QSettings()
        settings.setValue("device_address", value)

    @property
    def stimuli_monitor(self) -> str:
        settings = QSettings()
        return settings.value("stimuli_monitor", self._screens.screen_list[-1])

    @stimuli_monitor.setter
    def stimuli_monitor(self, value: str):
        settings = QSettings()
        settings.setValue("stimuli_monitor", value)

    @Slot()
    def on_device_address_changed(self):
        self.device_address = self._device_address.text()

    @Slot()
    def on_stimuli_monitor_changed(self, screen: str):
        self.stimuli_monitor = screen
