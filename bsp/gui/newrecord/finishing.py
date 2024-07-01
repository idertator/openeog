from PySide6 import QtWidgets

from bsp.core.logging import log
from bsp.gui.screens import ScreensManager
from bsp.settings import config

from .consts import SELECTOR_WIDTH


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

        self._record_name = QtWidgets.QLineEdit()
        self._record_name.setText("")
        self._record_name.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed,
        )
        self._record_name.textChanged.connect(self.on_record_name_changed)

        device_type = config.device_type
        if device_type not in config.DEVICE_TYPES:
            device_type = config.DEVICE_TYPES[-1]
            config.device_type = device_type

        self._device_type = QtWidgets.QComboBox()
        self._device_type.addItems(config.DEVICE_TYPES)
        self._device_type.setCurrentText(device_type)
        self._device_type.setFixedWidth(SELECTOR_WIDTH)
        self._device_type.currentTextChanged.connect(self.on_device_type_changed)

        self._device_address = QtWidgets.QLineEdit()
        self._device_address.setText(config.device_address)
        self._device_address.setFixedWidth(SELECTOR_WIDTH)
        self._device_address.textChanged.connect(self.on_device_address_changed)

        stimuli_monitor = config.stimuli_monitor or self._screens.screen_list[-1]
        if stimuli_monitor not in screens.screen_list:
            stimuli_monitor = screens.screen_list[-1]

        config.stimuli_monitor = stimuli_monitor

        self._stimuli_monitor = QtWidgets.QComboBox()
        self._stimuli_monitor.addItems(screens.screen_list)
        self._stimuli_monitor.setCurrentText(stimuli_monitor)
        self._stimuli_monitor.setFixedWidth(SELECTOR_WIDTH)
        self._stimuli_monitor.currentTextChanged.connect(
            self.on_stimuli_monitor_changed
        )

        self._stimuli_monitor_width = QtWidgets.QSpinBox()
        self._stimuli_monitor_width.setRange(0, 50000)
        self._stimuli_monitor_width.setValue(config.stimuli_monitor_width)
        self._stimuli_monitor_width.setSuffix(" mm")
        self._stimuli_monitor_width.setFixedWidth(100)
        self._stimuli_monitor_width.valueChanged.connect(
            self.on_stimuli_monitor_width_changed
        )

        self._stimuli_monitor_middle_label = QtWidgets.QLabel("x")

        self._stimuli_monitor_height = QtWidgets.QSpinBox()
        self._stimuli_monitor_height.setRange(0, 50000)
        self._stimuli_monitor_height.setValue(config.stimuli_monitor_height)
        self._stimuli_monitor_height.setSuffix(" mm")
        self._stimuli_monitor_height.setFixedWidth(100)
        self._stimuli_monitor_height.valueChanged.connect(
            self.on_stimuli_monitor_height_changed
        )

        self._stimuli_ball_ratio = QtWidgets.QSpinBox()
        self._stimuli_ball_ratio.setRange(0, 128)
        self._stimuli_ball_ratio.setValue(config.ball_ratio)
        self._stimuli_ball_ratio.setSuffix(" px")
        self._stimuli_ball_ratio.setFixedWidth(64)
        self._stimuli_ball_ratio.valueChanged.connect(
            self.on_stimuli_ball_ratio_changed
        )

        self._stimuli_monitor_layout = QtWidgets.QHBoxLayout()
        self._stimuli_monitor_layout.addWidget(self._stimuli_monitor_width)
        self._stimuli_monitor_layout.addWidget(self._stimuli_monitor_middle_label)
        self._stimuli_monitor_layout.addWidget(self._stimuli_monitor_height)
        self._stimuli_monitor_layout.addStretch()

        self._record_path_edit = QtWidgets.QLineEdit()
        self._record_path_edit.setText(config.record_path)
        self._record_path_edit.setReadOnly(True)
        self._record_path_edit.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed,
        )

        self._record_path_button = QtWidgets.QPushButton()
        self._record_path_button.setText("Select")
        self._record_path_button.clicked.connect(
            self.on_record_path_select_button_clicked
        )

        self._record_path_layout = QtWidgets.QHBoxLayout()
        self._record_path_layout.addWidget(self._record_path_edit)
        self._record_path_layout.addWidget(self._record_path_button)
        self._record_path_layout.setContentsMargins(0, 0, 0, 0)
        self._record_path_layout.setSpacing(0)

        layout = QtWidgets.QFormLayout()
        layout.addRow("Nombre del Registro", self._record_name)
        layout.addRow("Dispositivo", self._device_type)
        layout.addRow("Ruta del Dispositivo", self._device_address)
        layout.addRow("Pantalla de Estímulo", self._stimuli_monitor)
        layout.addRow("Tamaño Pantalla de Estímulo", self._stimuli_monitor_layout)
        layout.addRow("Tamaño del Estímulo", self._stimuli_ball_ratio)
        layout.addRow("Ruta del Registro", self._record_path_layout)

        self.setLayout(layout)

    def isComplete(self) -> bool:
        if self._record_name.text().strip() == "":
            return False

        if self._device_address.text().strip() == "":
            return False

        return True

    @property
    def record_name(self) -> str:
        return self._record_name.text()

    def on_record_name_changed(self):
        self.completeChanged.emit()

    def on_device_address_changed(self):
        config.device_address = self._device_address.text()
        self.completeChanged.emit()

    def on_stimuli_monitor_changed(self, screen: str):
        config.stimuli_monitor = screen

    def on_stimuli_monitor_width_changed(self):
        config.stimuli_monitor_width = self._stimuli_monitor_width.value()

    def on_stimuli_monitor_height_changed(self):
        config.stimuli_monitor_height = self._stimuli_monitor_height.value()

    def on_stimuli_ball_ratio_changed(self):
        config.ball_ratio = self._stimuli_ball_ratio.value()

    def on_device_type_changed(self, device_type: str):
        config.device_type = device_type

    def on_record_path_select_button_clicked(self):
        if record_path := QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Seleccione Ruta del Registro",
            config.record_path,
        ):
            config.record_path = record_path
            self._record_path_edit.setText(record_path)
            self.completeChanged.emit()
