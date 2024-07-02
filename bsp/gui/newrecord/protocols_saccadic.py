from os.path import dirname

from PySide6 import QtWidgets

from bsp.core import log
from bsp.core.models import SaccadicProtocolTemplate
from bsp.settings import config

from .consts import SELECTOR_WIDTH


class ProtocolsSaccadicPage(QtWidgets.QWizardPage):
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ):
        super().__init__(parent=parent)

        self.setTitle("Configure su registro de Sacádico")

        self._name_text = QtWidgets.QLineEdit(self)
        self._name_text.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed,
        )
        self._name_text.textChanged.connect(self.on_name_text_changed)

        self._calibration_length = QtWidgets.QSpinBox(self)
        self._calibration_length.setFixedWidth(SELECTOR_WIDTH)
        self._calibration_length.setMinimum(10)
        self._calibration_length.setMaximum(100)
        self._calibration_length.setSuffix(" segundos")

        self._calibration_count = QtWidgets.QSpinBox(self)
        self._calibration_count.setFixedWidth(SELECTOR_WIDTH)
        self._calibration_count.setMinimum(5)
        self._calibration_count.setMaximum(10)
        self._calibration_count.setSuffix(" sácadas")

        self._saccadic_length = QtWidgets.QSpinBox(self)
        self._saccadic_length.setFixedWidth(SELECTOR_WIDTH)
        self._saccadic_length.setMinimum(10)
        self._saccadic_length.setMaximum(100)
        self._saccadic_length.setSuffix(" segundos")

        self._saccadic_variability = QtWidgets.QDoubleSpinBox(self)
        self._saccadic_variability.setFixedWidth(SELECTOR_WIDTH)
        self._saccadic_variability.setMinimum(0.1)
        self._saccadic_variability.setMaximum(100.0)
        self._saccadic_variability.setSuffix("%")

        self._saccadic_count = QtWidgets.QSpinBox(self)
        self._saccadic_count.setFixedWidth(SELECTOR_WIDTH)
        self._saccadic_count.setMinimum(5)
        self._saccadic_count.setMaximum(30)
        self._saccadic_count.setSuffix(" sácadas")

        self._saccadic_replicas = QtWidgets.QCheckBox(self)

        self._saccadic_10 = QtWidgets.QCheckBox(self)
        self._saccadic_10.toggled.connect(self.on_saccadic_check_changed)

        self._saccadic_20 = QtWidgets.QCheckBox(self)
        self._saccadic_20.toggled.connect(self.on_saccadic_check_changed)

        self._saccadic_30 = QtWidgets.QCheckBox(self)
        self._saccadic_30.toggled.connect(self.on_saccadic_check_changed)

        self._saccadic_40 = QtWidgets.QCheckBox(self)
        self._saccadic_40.toggled.connect(self.on_saccadic_check_changed)

        self._saccadic_50 = QtWidgets.QCheckBox(self)
        self._saccadic_50.toggled.connect(self.on_saccadic_check_changed)

        self._saccadic_60 = QtWidgets.QCheckBox(self)
        self._saccadic_60.toggled.connect(self.on_saccadic_check_changed)

        self._form_layout = QtWidgets.QFormLayout(self)

        self._form_layout.addRow("Nombre", self._name_text)
        self._form_layout.addRow("Longitud Calibración", self._calibration_length)
        self._form_layout.addRow("Sácadas Calibración", self._calibration_count)
        self._form_layout.addRow("Longitud Sacádica", self._saccadic_length)
        self._form_layout.addRow("Variabilidad Sacádica", self._saccadic_variability)
        self._form_layout.addRow("Sácadas", self._saccadic_count)
        self._form_layout.addRow("Incluir Réplicas", self._saccadic_replicas)
        self._form_layout.addRow("Sacádica 10°", self._saccadic_10)
        self._form_layout.addRow("Sacádica 20°", self._saccadic_20)
        self._form_layout.addRow("Sacádica 30°", self._saccadic_30)
        self._form_layout.addRow("Sacádica 40°", self._saccadic_40)
        self._form_layout.addRow("Sacádica 50°", self._saccadic_50)
        self._form_layout.addRow("Sacádica 60°", self._saccadic_60)

        self.completeChanged.connect(self.on_complete_changed)

        self.setLayout(self._form_layout)

    def initializePage(self):
        if filename := config.saccadic_protocol_path:
            self._load_protocol_file(filename)

    def isComplete(self) -> bool:
        try:
            self.validate()
            return True
        except ValueError:
            return False

    @property
    def protocol_template(self) -> SaccadicProtocolTemplate:
        return SaccadicProtocolTemplate(
            name=self._name_text.text().strip(),
            calibration_length=self._calibration_length.value(),
            calibration_count=self._calibration_count.value(),
            saccadic_length=self._saccadic_length.value(),
            saccadic_variability=self._saccadic_variability.value(),
            saccadic_count=self._saccadic_count.value(),
            include_replicas=self._saccadic_replicas.isChecked(),
            saccadic_10=self._saccadic_10.isChecked(),
            saccadic_20=self._saccadic_20.isChecked(),
            saccadic_30=self._saccadic_30.isChecked(),
            saccadic_40=self._saccadic_40.isChecked(),
            saccadic_50=self._saccadic_50.isChecked(),
            saccadic_60=self._saccadic_60.isChecked(),
        )

    def validate(self):
        if self._name_text.text().strip() == "":
            raise ValueError("El nombre no puede estar vacío")

        if not any(
            [
                self._saccadic_10.isChecked(),
                self._saccadic_20.isChecked(),
                self._saccadic_30.isChecked(),
                self._saccadic_40.isChecked(),
                self._saccadic_50.isChecked(),
                self._saccadic_60.isChecked(),
            ]
        ):
            raise ValueError("Debe seleccionar al menos una prueba sacádica")

    def _load_protocol_file(self, filename: str):
        try:
            protocol_template = SaccadicProtocolTemplate.open(filename)

            self._name_text.setText(protocol_template.name)
            self._calibration_length.setValue(protocol_template.calibration_length)
            self._calibration_count.setValue(protocol_template.calibration_count)
            self._saccadic_length.setValue(protocol_template.saccadic_length)
            self._saccadic_variability.setValue(protocol_template.saccadic_variability)
            self._saccadic_count.setValue(protocol_template.saccadic_count)
            self._saccadic_replicas.setChecked(protocol_template.include_replicas)
            self._saccadic_10.setChecked(protocol_template.saccadic_10)
            self._saccadic_20.setChecked(protocol_template.saccadic_20)
            self._saccadic_30.setChecked(protocol_template.saccadic_30)
            self._saccadic_40.setChecked(protocol_template.saccadic_40)
            self._saccadic_50.setChecked(protocol_template.saccadic_50)
            self._saccadic_60.setChecked(protocol_template.saccadic_60)

        except ValueError as e:
            log.error(str(e))
            QtWidgets.QMessageBox.critical(
                self,
                "Formato inválido",
                str(e),
            )

    def load_protocol(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Cargar Protocolo",
            config.protocols_path,
            "Protocolo (*.json)",
        )
        if filename:
            self._load_protocol_file(filename)

    def save_protocol(self):
        default_path = "{dir}/{name}.json".format(
            dir=config.protocols_path,
            name=self._name_text.text().strip(),
        )

        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Guardar Protocolo",
            default_path,
            "Protocolo (*.json)",
        )

        if filename:
            self.protocol_template.save(filename)
            config.protocols_path = dirname(filename)
            config.saccadic_protocol_path = filename

            QtWidgets.QMessageBox.information(
                self,
                "Protocolo guardado",
                f"Protocolo guardado en {filename}",
            )

    def on_name_text_changed(self):
        self.completeChanged.emit()

    def on_saccadic_check_changed(self):
        self.completeChanged.emit()

    def on_complete_changed(self):
        wizard = self.wizard()
        save_button = wizard.button(QtWidgets.QWizard.CustomButton2)
        save_button.setEnabled(self.isComplete())
