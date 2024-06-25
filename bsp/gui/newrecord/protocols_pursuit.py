from json import dump, load
from os.path import dirname

from PySide6 import QtWidgets

from bsp.core import Protocol, log
from bsp.settings import config


class ProtocolsPursuitPage(QtWidgets.QWizardPage):
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ):
        super().__init__(parent=parent)

        self.setTitle("Configure su registro de Persecución Suave")

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

        self._pursuit_length = QtWidgets.QSpinBox(self)
        self._pursuit_length.setMinimumWidth(105)
        self._pursuit_length.setMinimum(10)
        self._pursuit_length.setMaximum(100)
        self._pursuit_length.setSuffix(" segundos")

        self._pursuit_speed = QtWidgets.QDoubleSpinBox(self)
        self._pursuit_speed.setMinimumWidth(105)
        self._pursuit_speed.setMinimum(0.1)
        self._pursuit_speed.setMaximum(10.0)
        self._pursuit_speed.setSuffix("°/segundo")

        self._pursuit_replicas = QtWidgets.QCheckBox(self)

        self._pursuit_10 = QtWidgets.QCheckBox(self)
        self._pursuit_10.toggled.connect(self._on_pursuit_check_changed)

        self._pursuit_20 = QtWidgets.QCheckBox(self)
        self._pursuit_20.toggled.connect(self._on_pursuit_check_changed)

        self._pursuit_30 = QtWidgets.QCheckBox(self)
        self._pursuit_30.toggled.connect(self._on_pursuit_check_changed)

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
    def json(self) -> dict:
        return {
            "type": Protocol.Pursuit,
            "name": self._name_text.text().strip(),
            "calibration_length": self._calibration_length.value(),
            "calibration_count": self._calibration_count.value(),
            "pursuit_length": self._pursuit_length.value(),
            "pursuit_speed": self._pursuit_speed.value(),
            "include_replicas": self._pursuit_replicas.isChecked(),
            "pursuit_10": self._pursuit_10.isChecked(),
            "pursuit_20": self._pursuit_20.isChecked(),
            "pursuit_30": self._pursuit_30.isChecked(),
            "pursuit_60": self._pursuit_60.isChecked(),
        }

    def validate(self):
        if self._name_text.text().strip() == "":
            raise ValueError("El nombre no puede estar vacío")

        if not any(
            [
                self._pursuit_10.isChecked(),
                self._pursuit_20.isChecked(),
                self._pursuit_30.isChecked(),
                self._pursuit_60.isChecked(),
            ]
        ):
            raise ValueError("Debe seleccionar al menos una prueba de persecución")

    def _validate_type(self, json: dict) -> Protocol:
        test_type = json.get("type", None)
        if test_type not in iter(Protocol):
            raise ValueError(f"Tipo de prueba inválido: {test_type}")

        test_type = Protocol(test_type)
        if test_type != Protocol.Pursuit:
            raise ValueError(f"Tipo de prueba inválido: {test_type}")

        return test_type

    def _validate_name(self, json: dict) -> str:
        name = json.get("name", None)
        if not isinstance(name, str) or not name:
            raise ValueError(f"El nombre {name} no es válido")

        return name

    def _validate_calibration_length(self, json: dict) -> float:
        calibration_length = json.get("calibration_length", None)
        if not isinstance(calibration_length, (int, float)):
            raise ValueError(f"Longitud de calibración inválida: {calibration_length}")

        if calibration_length < 10 or calibration_length > 100:
            raise ValueError(f"Longitud de calibración inválida: {calibration_length}")

        return float(calibration_length)

    def _validate_calibration_count(self, json: dict) -> int:
        calibration_count = json.get("calibration_count", None)
        if not isinstance(calibration_count, (int, float)):
            raise ValueError(f"Longitud de calibración inválida: {calibration_count}")

        if calibration_count < 5 or calibration_count > 10:
            raise ValueError(f"Longitud de calibración inválida: {calibration_count}")

        return int(calibration_count)

    def _validate_pursuit_length(self, json: dict) -> float:
        pursuit_length = json.get("pursuit_length", None)
        if not isinstance(pursuit_length, (int, float)):
            raise ValueError("Longitud de persecución inválida")

        if pursuit_length < 10 or pursuit_length > 100:
            raise ValueError("Longitud de persecución inválida")

        return float(pursuit_length)

    def _validate_pursuit_speed(self, json: dict) -> float:
        pursuit_speed = json.get("pursuit_speed", None)
        if not isinstance(pursuit_speed, (int, float)):
            raise ValueError("Variabilidad sacádica inválida")

        if pursuit_speed < 0.1 or pursuit_speed > 10.0:
            raise ValueError("Variabilidad sacádica inválida")

        return float(pursuit_speed)

    def _load_protocol_file(self, filename: str):
        log.debug(f"Loading protocol: {filename}")

        json = {}
        with open(filename, "rt") as f:
            json = load(f)

        try:
            self._validate_type(json)

            self._name_text.setText(
                self._validate_name(json),
            )
            self._calibration_length.setValue(
                self._validate_calibration_length(json),
            )
            self._calibration_count.setValue(
                self._validate_calibration_count(json),
            )
            self._pursuit_length.setValue(
                self._validate_pursuit_length(json),
            )
            self._pursuit_speed.setValue(
                self._validate_pursuit_speed(json),
            )
            self._pursuit_replicas.setChecked(json["include_replicas"])
            self._pursuit_10.setChecked(json["pursuit_10"])
            self._pursuit_20.setChecked(json["pursuit_20"])
            self._pursuit_30.setChecked(json["pursuit_30"])
            self._pursuit_60.setChecked(json["pursuit_60"])

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
            with open(filename, "wt") as f:
                dump(self.json, f, indent=4)

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
