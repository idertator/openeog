from os.path import dirname

from PySide6 import QtWidgets

from openeog.core import log
from openeog.core.models import PursuitProtocolTemplate
from openeog.settings import config

from .consts import SELECTOR_WIDTH


class ProtocolsPursuitPage(QtWidgets.QWizardPage):
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ):
        super().__init__(parent=parent)

        self.setTitle("Configure su registro de Persecución Suave")

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

        self._pursuit_length = QtWidgets.QSpinBox(self)
        self._pursuit_length.setFixedWidth(SELECTOR_WIDTH)
        self._pursuit_length.setMinimum(10)
        self._pursuit_length.setMaximum(100)
        self._pursuit_length.setSuffix(" segundos")

        self._pursuit_speed = QtWidgets.QDoubleSpinBox(self)
        self._pursuit_speed.setFixedWidth(SELECTOR_WIDTH)
        self._pursuit_speed.setMinimum(0.1)
        self._pursuit_speed.setMaximum(100.0)
        self._pursuit_speed.setSuffix("°/segundo")

        self._pursuit_replicas = QtWidgets.QCheckBox(self)

        self._pursuit_10 = QtWidgets.QCheckBox(self)
        self._pursuit_10.toggled.connect(self._on_pursuit_check_changed)

        self._pursuit_20 = QtWidgets.QCheckBox(self)
        self._pursuit_20.toggled.connect(self._on_pursuit_check_changed)

        self._pursuit_30 = QtWidgets.QCheckBox(self)
        self._pursuit_30.toggled.connect(self._on_pursuit_check_changed)

        self._pursuit_40 = QtWidgets.QCheckBox(self)
        self._pursuit_40.toggled.connect(self._on_pursuit_check_changed)

        self._pursuit_50 = QtWidgets.QCheckBox(self)
        self._pursuit_50.toggled.connect(self._on_pursuit_check_changed)

        self._pursuit_60 = QtWidgets.QCheckBox(self)
        self._pursuit_60.toggled.connect(self._on_pursuit_check_changed)

        self._form_layout = QtWidgets.QFormLayout(self)

        self._form_layout.addRow("Nombre", self._name_text)
        self._form_layout.addRow("Longitud Calibración", self._calibration_length)
        self._form_layout.addRow("Sácadas Calibración", self._calibration_count)
        self._form_layout.addRow("Longitud de la Persecución", self._pursuit_length)
        self._form_layout.addRow("Velocidad Persecución", self._pursuit_speed)
        self._form_layout.addRow("Incluir Réplicas", self._pursuit_replicas)
        self._form_layout.addRow("Persecución 10°", self._pursuit_10)
        self._form_layout.addRow("Persecución 20°", self._pursuit_20)
        self._form_layout.addRow("Persecución 30°", self._pursuit_30)
        self._form_layout.addRow("Persecución 40°", self._pursuit_40)
        self._form_layout.addRow("Persecución 50°", self._pursuit_50)
        self._form_layout.addRow("Persecución 60°", self._pursuit_60)

        self.completeChanged.connect(self.on_complete_changed)

        self.setLayout(self._form_layout)

    def initializePage(self):
        if filename := config.pursuit_protocol_path:
            self._load_protocol_file(filename)

    def isComplete(self) -> bool:
        try:
            self.validate()
            return True
        except ValueError:
            return False

    @property
    def protocol_template(self) -> PursuitProtocolTemplate:
        return PursuitProtocolTemplate(
            name=self._name_text.text().strip(),
            calibration_length=self._calibration_length.value(),
            calibration_count=self._calibration_count.value(),
            pursuit_length=self._pursuit_length.value(),
            pursuit_speed=self._pursuit_speed.value(),
            include_replicas=self._pursuit_replicas.isChecked(),
            pursuit_10=self._pursuit_10.isChecked(),
            pursuit_20=self._pursuit_20.isChecked(),
            pursuit_30=self._pursuit_30.isChecked(),
            pursuit_40=self._pursuit_40.isChecked(),
            pursuit_50=self._pursuit_50.isChecked(),
            pursuit_60=self._pursuit_60.isChecked(),
        )

    def validate(self):
        if self._name_text.text().strip() == "":
            raise ValueError("El nombre no puede estar vacío")

        if not any(
            [
                self._pursuit_10.isChecked(),
                self._pursuit_20.isChecked(),
                self._pursuit_30.isChecked(),
                self._pursuit_40.isChecked(),
                self._pursuit_50.isChecked(),
                self._pursuit_60.isChecked(),
            ]
        ):
            raise ValueError("Debe seleccionar al menos una prueba de persecución")

    def _load_protocol_file(self, filename: str):
        try:
            protocol_template = PursuitProtocolTemplate.open(filename)

            self._name_text.setText(protocol_template.name)
            self._calibration_length.setValue(protocol_template.calibration_length)
            self._calibration_count.setValue(protocol_template.calibration_count)
            self._pursuit_length.setValue(protocol_template.pursuit_length)
            self._pursuit_speed.setValue(protocol_template.pursuit_speed)
            self._pursuit_replicas.setChecked(protocol_template.include_replicas)
            self._pursuit_10.setChecked(protocol_template.pursuit_10)
            self._pursuit_20.setChecked(protocol_template.pursuit_20)
            self._pursuit_30.setChecked(protocol_template.pursuit_30)
            self._pursuit_40.setChecked(protocol_template.pursuit_40)
            self._pursuit_50.setChecked(protocol_template.pursuit_50)
            self._pursuit_60.setChecked(protocol_template.pursuit_60)

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
            config.pursuit_protocol_path = filename

            QtWidgets.QMessageBox.information(
                self,
                "Protocolo guardado",
                f"Protocolo guardado en {filename}",
            )

    def on_name_text_changed(self):
        self.completeChanged.emit()

    def _on_pursuit_check_changed(self):
        self.completeChanged.emit()

    def on_complete_changed(self):
        wizard = self.wizard()
        save_button = wizard.button(QtWidgets.QWizard.CustomButton2)
        save_button.setEnabled(self.isComplete())
