from PySide6 import QtWidgets


class FinishingPage(QtWidgets.QWizardPage):
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ):
        super().__init__(parent=parent)

        self.setTitle("Finalizando la Configuración")
        self.setFinalPage(True)
