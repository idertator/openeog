from PySide6 import QtWidgets
from PySide6.QtCore import QSize, Qt, Slot
from PySide6.QtGui import QIcon

from bsp.core import Protocol, log
from bsp.gui.config import PROTOCOLS


class ProtocolsPage(QtWidgets.QWizardPage):
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ):
        super().__init__(parent=parent)
        self.setTitle("Seleccione Protocolo")

        self._buttons_layout = QtWidgets.QVBoxLayout()
        self._buttons_group = QtWidgets.QButtonGroup()
        self._buttons_group.setExclusive(True)
        self._buttons_group.buttonClicked.connect(self.on_protocol_button_clicked)

        self._protocols = {}

        for idx, protocol in enumerate(PROTOCOLS):
            label = QtWidgets.QLabel(protocol["name"])
            label.setAlignment(Qt.AlignCenter)
            label.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Fixed,
            )

            button = QtWidgets.QPushButton()
            button.setIcon(QIcon(protocol["icon"]))
            button.setSizePolicy(
                QtWidgets.QSizePolicy.Fixed,
                QtWidgets.QSizePolicy.Fixed,
            )
            button.setFixedSize(250, 100)
            button.setIconSize(QSize(250, 100))
            button.setCheckable(True)
            button.setAutoDefault(False)

            self._buttons_group.addButton(button)
            self._buttons_layout.addWidget(label)
            self._buttons_layout.addWidget(button)

            self._protocols[id(button)] = protocol["protocol"]

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.addStretch()
        self._layout.addLayout(self._buttons_layout)
        self._layout.addStretch()

        self.setLayout(self._layout)

    def isComplete(self) -> bool:
        for button in self._buttons_group.buttons():
            if button.isChecked():
                return True
        return False

    @Slot()
    def on_protocol_button_clicked(self, button: QtWidgets.QPushButton):
        protocol = self._protocols[id(button)]
        log.debug(f"Selected protocol: {protocol}")
        self.completeChanged.emit()

    @property
    def protocol(self) -> Protocol:
        for button in self._buttons_group.buttons():
            if button.isChecked():
                protocol = self._protocols[id(button)]
                return protocol
