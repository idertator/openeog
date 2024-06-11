from PySide6 import QtWidgets

from bsp.core import log


class ProtocolsSaccadicPage(QtWidgets.QWizardPage):
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ):
        super().__init__(parent=parent)

        self.setTitle("Configure su registro de Sacádico")

        self._name_text = QtWidgets.QLineEdit(self)

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
        self._saccadic_20 = QtWidgets.QCheckBox(self)
        self._saccadic_30 = QtWidgets.QCheckBox(self)
        self._saccadic_60 = QtWidgets.QCheckBox(self)

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

        self.setLayout(self._form_layout)

    def initializePage(self):
        wizard = self.wizard()
        wizard.setButtonLayout(
            [
                QtWidgets.QWizard.CustomButton1,
                QtWidgets.QWizard.CustomButton2,
                QtWidgets.QWizard.Stretch,
                QtWidgets.QWizard.CancelButton,
                QtWidgets.QWizard.BackButton,
                QtWidgets.QWizard.NextButton,
            ]
        )

    @property
    def json(self) -> dict:
        pass

    def validate(self):
        # Lanzar ValueError si ocurren problemas de validación
        pass

    def load_protocol(self):
        log.debug("Load protocol")

    def save_protocol(self):
        log.debug("Save protocol")
