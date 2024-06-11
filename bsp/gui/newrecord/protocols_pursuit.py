from PySide6 import QtWidgets


class ProtocolsPursuitPage(QtWidgets.QWizardPage):
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ):
        super().__init__(parent=parent)

        self.setTitle("Configure su registro de Persecución Suave")

    def initializePage(self):
        wizard = self.wizard()
        wizard.setButtonLayout(
            [
                QtWidgets.QWizard.Stretch,
                QtWidgets.QWizard.CancelButton,
                QtWidgets.QWizard.BackButton,
                QtWidgets.QWizard.NextButton,
            ]
        )
