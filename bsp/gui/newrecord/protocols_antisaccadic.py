from PySide6 import QtWidgets


class ProtocolsAntisaccadicPage(QtWidgets.QWizardPage):
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ):
        super().__init__(parent=parent)

        self.setTitle("Configure su registro Antisacádico")

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
