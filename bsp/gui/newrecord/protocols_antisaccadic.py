from json import dump, load
from os.path import dirname

from PySide6 import QtWidgets

from bsp.core import Protocol, log
from bsp.settings import config


class ProtocolsAntisaccadicPage(QtWidgets.QWizardPage):
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ):
        super().__init__(parent=parent)

        self.setTitle("Configure su registro de Antisacádico")

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
    def json(self) -> dict:
        return {
            "type": Protocol.Antisaccadic,
            "name": self._name_text.text().strip(),
            "calibration_length": self._calibration_length.value(),
            "calibration_count": self._calibration_count.value(),
            "antisaccadic_length": self._antisaccadic_length.value(),
            "antisaccadic_variability": self._antisaccadic_variability.value(),
            "antisaccadic_count": self._antisaccadic_count.value(),
            "include_replicas": self._antisaccadic_replicas.isChecked(),
            "antisaccadic_10": self._antisaccadic_10.isChecked(),
            "antisaccadic_20": self._antisaccadic_20.isChecked(),
            "antisaccadic_30": self._antisaccadic_30.isChecked(),
            "antisaccadic_60": self._antisaccadic_60.isChecked(),
        }

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

    def _validate_type(self, json: dict) -> Protocol:
        test_type = json.get("type", None)
        if test_type not in iter(Protocol):
            raise ValueError(f"Tipo de prueba inválido: {test_type}")

        test_type = Protocol(test_type)
        if test_type != Protocol.Antisaccadic:
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

    def _validate_antisaccadic_length(self, json: dict) -> float:
        antisaccadic_length = json.get("antisaccadic_length", None)
        if not isinstance(antisaccadic_length, (int, float)):
            raise ValueError("Longitud antisacádica inválida")

        if antisaccadic_length < 10 or antisaccadic_length > 100:
            raise ValueError("Longitud antisacádica inválida")

        return float(antisaccadic_length)

    def _validate_antisaccadic_variability(self, json: dict) -> float:
        antisaccadic_variability = json.get("antisaccadic_variability", None)
        if not isinstance(antisaccadic_variability, (int, float)):
            raise ValueError("Variabilidad antisacádica inválida")

        if antisaccadic_variability < 0.1 or antisaccadic_variability > 100:
            raise ValueError("Variabilidad antisacádica inválida")

        return float(antisaccadic_variability)

    def _validate_antisaccadic_count(self, json: dict) -> int:
        antisaccadic_count = json.get("antisaccadic_count", None)
        if not isinstance(antisaccadic_count, (int, float)):
            raise ValueError(f"Cantidad de antisácadas inválida: {antisaccadic_count}")

        if antisaccadic_count < 5 or antisaccadic_count > 30:
            raise ValueError(f"Cantidad de antisácadas inválida: {antisaccadic_count}")

        return int(antisaccadic_count)

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
            self._antisaccadic_length.setValue(
                self._validate_antisaccadic_length(json),
            )
            self._antisaccadic_variability.setValue(
                self._validate_antisaccadic_variability(json),
            )
            self._antisaccadic_count.setValue(
                self._validate_antisaccadic_count(json),
            )
            self._antisaccadic_replicas.setChecked(json["include_replicas"])
            self._antisaccadic_10.setChecked(json["antisaccadic_10"])
            self._antisaccadic_20.setChecked(json["antisaccadic_20"])
            self._antisaccadic_30.setChecked(json["antisaccadic_30"])
            self._antisaccadic_60.setChecked(json["antisaccadic_60"])

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
