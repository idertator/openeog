from json import dump, load

from PySide6 import QtWidgets

from bsp import settings
from bsp.core import Protocol, log


class ProtocolsSaccadicPage(QtWidgets.QWizardPage):
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ):
        super().__init__(parent=parent)

        self.setTitle("Configure su registro de Sacádico")

        self._name_text = QtWidgets.QLineEdit(self)
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

        self._saccadic_length = QtWidgets.QSpinBox(self)
        self._saccadic_length.setMinimumWidth(105)
        self._saccadic_length.setMinimum(10)
        self._saccadic_length.setMaximum(100)
        self._saccadic_length.setSuffix(" segundos")

        self._saccadic_variability = QtWidgets.QDoubleSpinBox(self)
        self._saccadic_variability.setMinimumWidth(105)
        self._saccadic_variability.setMinimum(0.1)
        self._saccadic_variability.setMaximum(100.0)
        self._saccadic_variability.setSuffix("%")

        self._saccadic_count = QtWidgets.QSpinBox(self)
        self._saccadic_count.setMinimumWidth(105)
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
        self._form_layout.addRow("Sacádica 60°", self._saccadic_60)

        self.completeChanged.connect(self.on_complete_changed)

        self.setLayout(self._form_layout)

    def initializePage(self):
        if filename := settings.default_saccadic_protocol_path():
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
            "type": Protocol.Saccadic,
            "name": self._name_text.text().strip(),
            "calibration_length": self._calibration_length.value(),
            "calibration_count": self._calibration_count.value(),
            "saccadic_length": self._saccadic_length.value(),
            "saccadic_variability": self._saccadic_variability.value(),
            "saccadic_count": self._saccadic_count.value(),
            "include_replicas": self._saccadic_replicas.isChecked(),
            "saccadic_10": self._saccadic_10.isChecked(),
            "saccadic_20": self._saccadic_20.isChecked(),
            "saccadic_30": self._saccadic_30.isChecked(),
            "saccadic_60": self._saccadic_60.isChecked(),
        }

    def validate(self):
        if self._name_text.text().strip() == "":
            raise ValueError("El nombre no puede estar vacío")

        if not any(
            [
                self._saccadic_10.isChecked(),
                self._saccadic_20.isChecked(),
                self._saccadic_30.isChecked(),
                self._saccadic_60.isChecked(),
            ]
        ):
            raise ValueError("Debe seleccionar al menos una prueba sacádica")

    def _validate_type(self, json: dict) -> Protocol:
        test_type = json.get("type", None)
        if test_type not in iter(Protocol):
            raise ValueError(f"Tipo de prueba inválido: {test_type}")

        test_type = Protocol(test_type)
        if test_type != Protocol.Saccadic:
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

    def _validate_saccadic_length(self, json: dict) -> float:
        saccadic_length = json.get("saccadic_length", None)
        if not isinstance(saccadic_length, (int, float)):
            raise ValueError("Longitud sacádica inválida")

        if saccadic_length < 10 or saccadic_length > 100:
            raise ValueError("Longitud sacádica inválida")

        return float(saccadic_length)

    def _validate_saccadic_variability(self, json: dict) -> float:
        saccadic_variability = json.get("saccadic_variability", None)
        if not isinstance(saccadic_variability, (int, float)):
            raise ValueError("Variabilidad sacádica inválida")

        if saccadic_variability < 0.1 or saccadic_variability > 100:
            raise ValueError("Variabilidad sacádica inválida")

        return float(saccadic_variability)

    def _validate_saccadic_count(self, json: dict) -> int:
        saccadic_count = json.get("saccadic_count", None)
        if not isinstance(saccadic_count, (int, float)):
            raise ValueError(f"Cantidad de sácadas inválida: {saccadic_count}")

        if saccadic_count < 5 or saccadic_count > 30:
            raise ValueError(f"Cantidad de sácadas inválida: {saccadic_count}")

        return int(saccadic_count)

    def _load_protocol_file(self, filename: str):
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
            self._saccadic_length.setValue(
                self._validate_saccadic_length(json),
            )
            self._saccadic_variability.setValue(
                self._validate_saccadic_variability(json),
            )
            self._saccadic_count.setValue(
                self._validate_saccadic_count(json),
            )
            self._saccadic_replicas.setChecked(json["include_replicas"])
            self._saccadic_10.setChecked(json["saccadic_10"])
            self._saccadic_20.setChecked(json["saccadic_20"])
            self._saccadic_30.setChecked(json["saccadic_30"])
            self._saccadic_60.setChecked(json["saccadic_60"])

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
            settings.protocols_path(),
            "Protocolo (*.json)",
        )
        if filename:
            self._load_protocol_file(filename)

    def save_protocol(self):
        default_path = "{dir}/{name}.json".format(
            dir=settings.protocols_path(),
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

            settings.set_default_saccadic_protocol_path(filename)

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
