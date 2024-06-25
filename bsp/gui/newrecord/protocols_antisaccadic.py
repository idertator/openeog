from os.path import dirname

from PySide6 import QtWidgets

from bsp.core import log
from bsp.core.models import AntisaccadicProtocolTemplate
from bsp.settings import config


class ProtocolsAntisaccadicPage(QtWidgets.QWizardPage):
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ):
        super().__init__(parent=parent)

        self.setTitle("Configure su registro de Antisacádico")

        self._name_text = QtWidgets.QLineEdit(self)
        self._name_text.setFixedWidth(270)
        self._name_text.textChanged.connect(self.on_name_text_changed)

        self._calibration_length = QtWidgets.QSpinBox(self)
        self._calibration_length.setMinimumWidth(105)
        self._calibration_length.setMinimum(10)
        self._calibration_length.setMaximum(100)
        self._calibration_length.setSuffix(" segundos")

        self._calibration_count = QtWidgets.QSpinBox(self)
        self._calibration_count.setMinimumWidth(105)
        self._calibration_count.setMinimum(5)
        self._calibration_count.setMaximum(10)
        self._calibration_count.setSuffix(" sácadas")

        self._antisaccadic_length = QtWidgets.QSpinBox(self)
        self._antisaccadic_length.setMinimumWidth(105)
        self._antisaccadic_length.setMinimum(10)
        self._antisaccadic_length.setMaximum(100)
        self._antisaccadic_length.setSuffix(" segundos")

        self._antisaccadic_variability = QtWidgets.QDoubleSpinBox(self)
        self._antisaccadic_variability.setMinimumWidth(105)
        self._antisaccadic_variability.setMinimum(0.1)
        self._antisaccadic_variability.setMaximum(100.0)
        self._antisaccadic_variability.setSuffix("%")

        self._antisaccadic_count = QtWidgets.QSpinBox(self)
        self._antisaccadic_count.setMinimumWidth(105)
        self._antisaccadic_count.setMinimum(5)
        self._antisaccadic_count.setMaximum(30)
        self._antisaccadic_count.setSuffix(" antisácadas")

        self._antisaccadic_replicas = QtWidgets.QCheckBox(self)

        self._antisaccadic_10 = QtWidgets.QCheckBox(self)
        self._antisaccadic_10.toggled.connect(self.on_saccadic_check_changed)

        self._antisaccadic_20 = QtWidgets.QCheckBox(self)
        self._antisaccadic_20.toggled.connect(self.on_saccadic_check_changed)

        self._antisaccadic_30 = QtWidgets.QCheckBox(self)
        self._antisaccadic_30.toggled.connect(self.on_saccadic_check_changed)

        self._antisaccadic_60 = QtWidgets.QCheckBox(self)
        self._antisaccadic_60.toggled.connect(self.on_saccadic_check_changed)

        self._form_layout = QtWidgets.QFormLayout(self)

        self._form_layout.addRow("Nombre", self._name_text)
        self._form_layout.addRow("Longitud Calibración", self._calibration_length)
        self._form_layout.addRow("Sácadas Calibración", self._calibration_count)
        self._form_layout.addRow("Longitud Antisacádica", self._antisaccadic_length)
        self._form_layout.addRow(
            "Variabilidad Antisacádica", self._antisaccadic_variability
        )
        self._form_layout.addRow("Antisácadas", self._antisaccadic_count)
        self._form_layout.addRow("Incluir Réplicas", self._antisaccadic_replicas)
        self._form_layout.addRow("Antisacádica 10°", self._antisaccadic_10)
        self._form_layout.addRow("Antisacádica 20°", self._antisaccadic_20)
        self._form_layout.addRow("Antisacádica 30°", self._antisaccadic_30)
        self._form_layout.addRow("Antisacádica 60°", self._antisaccadic_60)

        self.completeChanged.connect(self.on_complete_changed)

        self.setLayout(self._form_layout)

    def initializePage(self):
        if filename := config.antisaccadic_protocol_path:
            self._load_protocol_file(filename)

    def isComplete(self) -> bool:
        try:
            self.validate()
            return True
        except ValueError:
            return False

    @property
    def protocol_template(self) -> AntisaccadicProtocolTemplate:
        return AntisaccadicProtocolTemplate(
            name=self._name_text.text().strip(),
            calibration_length=self._calibration_length.value(),
            calibration_count=self._calibration_count.value(),
            antisaccadic_length=self._antisaccadic_length.value(),
            antisaccadic_variability=self._antisaccadic_variability.value(),
            antisaccadic_count=self._antisaccadic_count.value(),
            include_replicas=self._antisaccadic_replicas.isChecked(),
            antisaccadic_10=self._antisaccadic_10.isChecked(),
            antisaccadic_20=self._antisaccadic_20.isChecked(),
            antisaccadic_30=self._antisaccadic_30.isChecked(),
            antisaccadic_60=self._antisaccadic_60.isChecked(),
        )

    def validate(self):
        if self._name_text.text().strip() == "":
            raise ValueError("El nombre no puede estar vacío")

        if not any(
            [
                self._antisaccadic_10.isChecked(),
                self._antisaccadic_20.isChecked(),
                self._antisaccadic_30.isChecked(),
                self._antisaccadic_60.isChecked(),
            ]
        ):
            raise ValueError("Debe seleccionar al menos una prueba antisacádica")

    def _load_protocol_file(self, filename: str):
        try:
            protocol_template = AntisaccadicProtocolTemplate.open(filename)

            self._name_text.setText(protocol_template.name)
            self._calibration_length.setValue(protocol_template.calibration_length)
            self._calibration_count.setValue(protocol_template.calibration_count)
            self._antisaccadic_length.setValue(protocol_template.antisaccadic_length)
            self._antisaccadic_variability.setValue(
                protocol_template.antisaccadic_variability
            )
            self._antisaccadic_count.setValue(protocol_template.antisaccadic_count)
            self._antisaccadic_replicas.setChecked(protocol_template.include_replicas)
            self._antisaccadic_10.setChecked(protocol_template.antisaccadic_10)
            self._antisaccadic_20.setChecked(protocol_template.antisaccadic_20)
            self._antisaccadic_30.setChecked(protocol_template.antisaccadic_30)
            self._antisaccadic_60.setChecked(protocol_template.antisaccadic_60)

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
            config.antisaccadic_protocol_path = filename

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
