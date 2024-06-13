from sys import exit

from PySide6 import QtCore, QtGui, QtWidgets

from bsp.core import Protocol, log

from .finishing import FinishingPage
from .protocols import ProtocolsPage
from .protocols_antisaccadic import ProtocolsAntisaccadicPage
from .protocols_pursuit import ProtocolsPursuitPage
from .protocols_saccadic import ProtocolsSaccadicPage


class NewRecordWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(
            self.windowFlags()
            & ~QtCore.Qt.WindowCloseButtonHint
            & ~QtCore.Qt.WindowMaximizeButtonHint
        )
        self.setWindowFlag(QtCore.Qt.CustomizeWindowHint, True)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint, True)
        self.setWindowFlag(QtCore.Qt.WindowSystemMenuHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMinMaxButtonsHint, False)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

        self.setButtonText(QtWidgets.QWizard.CustomButton1, "Cargar")
        self.setButtonText(QtWidgets.QWizard.CustomButton2, "Guardar")
        self.setButtonText(QtWidgets.QWizard.CancelButton, "Cancelar")
        self.setButtonText(QtWidgets.QWizard.NextButton, "Siguiente")
        self.setButtonText(QtWidgets.QWizard.BackButton, "Atrás")
        self.setButtonText(QtWidgets.QWizard.FinishButton, "Finalizar")
        self.setButtonText(QtWidgets.QWizard.HelpButton, "Ayuda")

        self._load_button = self.button(QtWidgets.QWizard.CustomButton1)
        self._load_button.clicked.connect(self.on_load_clicked)

        self._save_button = self.button(QtWidgets.QWizard.CustomButton2)
        self._save_button.clicked.connect(self.on_save_clicked)

        # Setting up pages
        self._protocols_page = ProtocolsPage(self)
        self._protocols_antisaccadic_page = ProtocolsAntisaccadicPage(self)
        self._protocols_pursuit_page = ProtocolsPursuitPage(self)
        self._protocols_saccadic_page = ProtocolsSaccadicPage(self)
        self._finishing_page = FinishingPage(self)

        self.addPage(self._protocols_page)  # ID 0
        self.addPage(self._protocols_saccadic_page)  # ID 1
        self.addPage(self._protocols_antisaccadic_page)  # ID 2
        self.addPage(self._protocols_pursuit_page)  # ID 3
        self.addPage(self._finishing_page)  # ID 4

        self.currentIdChanged.connect(self.on_current_id_changed)

        self.setStartId(0)

    def showEvent(self, event: QtGui.QShowEvent):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def nextId(self):
        current_id = self.currentId()
        if current_id == 0:  # PathSelectionPage ID
            protocol = self._protocols_page.protocol

            match protocol:
                case Protocol.Saccadic:
                    return 1  # ProtocolsSaccadicPage ID

                case Protocol.Antisaccadic:
                    return 2  # ProtocolsAntisaccadicPage ID

                case Protocol.Pursuit:
                    return 3  # ProtocolsPursuitPage ID

        return 4  # FinishingPage ID

    def reject(self):
        log.info("User cancelled the wizard")
        exit(0)

    def on_current_id_changed(self, id):
        if id == 0:
            self.setButtonLayout(
                [
                    QtWidgets.QWizard.Stretch,
                    QtWidgets.QWizard.CancelButton,
                    QtWidgets.QWizard.NextButton,
                ]
            )
        elif id in {1, 2, 3}:
            self.setButtonLayout(
                [
                    QtWidgets.QWizard.CustomButton1,
                    QtWidgets.QWizard.CustomButton2,
                    QtWidgets.QWizard.Stretch,
                    QtWidgets.QWizard.CancelButton,
                    QtWidgets.QWizard.BackButton,
                    QtWidgets.QWizard.NextButton,
                ]
            )
        else:
            self.setButtonLayout(
                [
                    QtWidgets.QWizard.Stretch,
                    QtWidgets.QWizard.CancelButton,
                    QtWidgets.QWizard.BackButton,
                    QtWidgets.QWizard.FinishButton,
                ]
            )

    def on_load_clicked(self):
        if self.currentId() in {1, 2, 3}:
            page = self.currentPage()
            page.load_protocol()

    def on_save_clicked(self):
        if self.currentId() in {1, 2, 3}:
            page = self.currentPage()
            page.save_protocol()
