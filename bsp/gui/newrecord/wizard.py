from PySide6 import QtCore, QtGui, QtWidgets

from .protocols import ProtocolsPage


class NewRecordWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Remove the close and maximize buttons using window flags
        self.setWindowFlags(
            self.windowFlags()
            & ~QtCore.Qt.WindowCloseButtonHint
            & ~QtCore.Qt.WindowMaximizeButtonHint
        )
        # Alternatively, customize window hints for macOS
        self.setWindowFlag(QtCore.Qt.CustomizeWindowHint, True)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint, True)
        self.setWindowFlag(QtCore.Qt.WindowSystemMenuHint, True)
        # Remove close and maximize button
        self.setWindowFlag(QtCore.Qt.WindowMinMaxButtonsHint, False)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

        self._protocols_page = ProtocolsPage(self)

        self.setButtonText(QtWidgets.QWizard.CancelButton, "Cancelar")
        self.setButtonText(QtWidgets.QWizard.NextButton, "Siguiente")
        self.setButtonText(QtWidgets.QWizard.BackButton, "Atrás")
        self.setButtonText(QtWidgets.QWizard.FinishButton, "Finalizar")
        self.setButtonText(QtWidgets.QWizard.HelpButton, "Ayuda")

        self.addPage(self._protocols_page)

    def showEvent(self, event: QtGui.QShowEvent):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
