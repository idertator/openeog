from PySide6 import QtWidgets

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

        device_type = config.device_type
        if device_type not in config.DEVICE_TYPES:
            device_type = config.DEVICE_TYPES[-1]
            config.device_type = device_type

        self._device_type = QtWidgets.QComboBox()
        self._device_type.addItems(config.DEVICE_TYPES)
        self._device_type.setCurrentText(device_type)
        self._device_type.currentTextChanged.connect(self.on_device_type_changed)

        self._device_address = QtWidgets.QLineEdit()
        self._device_address.setText(config.device_address)
        self._device_address.textChanged.connect(self.on_device_address_changed)

        stimuli_monitor = config.stimuli_monitor or self._screens.screen_list[-1]
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

    def on_device_address_changed(self):
        config.device_address = self._device_address.text()

    def on_stimuli_monitor_changed(self, screen: str):
        config.stimuli_monitor = screen

    def on_device_type_changed(self, device_type: str):
        config.device_type = device_type
