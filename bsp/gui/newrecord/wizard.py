from PySide6 import QtWidgets

from .protocols import ProtocolsPage


class NewRecordWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._protocols_page = ProtocolsPage(self)

        self.setButtonText(QtWidgets.QWizard.CancelButton, "Cancelar")
        self.setButtonText(QtWidgets.QWizard.NextButton, "Siguiente")
        self.setButtonText(QtWidgets.QWizard.BackButton, "Atrás")
        self.setButtonText(QtWidgets.QWizard.FinishButton, "Finalizar")
        self.setButtonText(QtWidgets.QWizard.HelpButton, "Ayuda")

        self.addPage(self._protocols_page)
