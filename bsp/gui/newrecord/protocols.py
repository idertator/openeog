from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Property
from PySide6.QtGui import QIcon

from bsp import settings
from bsp.core import Protocol, log
from bsp.gui.config import PROTOCOLS


class ProtocolsPage(QtWidgets.QWizardPage):
    protocol_changed = QtCore.Signal(Protocol)

    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ):
        super().__init__(parent=parent)

        self.setTitle("Seleccione Protocolo")

        self._protocol: Protocol | None = None

        self._buttons_layout = QtWidgets.QVBoxLayout()
        self._buttons_group = QtWidgets.QButtonGroup()
        self._buttons_group.setExclusive(True)
        self._buttons_group.buttonClicked.connect(self.on_protocol_button_clicked)

        for idx, protocol in enumerate(PROTOCOLS):
            label = QtWidgets.QLabel(protocol["name"])
            label.setAlignment(QtCore.Qt.AlignCenter)
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
            button.setIconSize(QtCore.QSize(250, 100))
            button.setCheckable(True)
            button.setAutoDefault(False)

            self._buttons_group.addButton(button, idx)
            self._buttons_layout.addWidget(label)
            self._buttons_layout.addWidget(button)

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.addStretch()
        self._layout.addLayout(self._buttons_layout)
        self._layout.addStretch()

        self.setLayout(self._layout)

        self.registerField("protocol*", self, "protocol")

    def _protocolIdx(self, value: Protocol) -> int:
        for idx, protocol in enumerate(PROTOCOLS):
            if protocol["protocol"] == value:
                return idx
        return 0

    def initializePage(self):
        self.protocol = settings.default_selected_protocol()
        self.setField("protocol", self.protocol)
        button = self._buttons_group.button(self._protocolIdx(self.protocol))
        button.setChecked(True)

    def isComplete(self) -> bool:
        return self._protocol is not None

    @Property(str)
    def protocol(self) -> Protocol | None:
        return self._protocol

    @protocol.setter
    def protocol(self, protocol: Protocol | None):
        self._protocol = protocol
        self.protocol_changed.emit(protocol)

    def on_protocol_button_clicked(self, button: QtWidgets.QPushButton):
        idx = self._buttons_group.id(button)
        protocol = PROTOCOLS[idx]["protocol"]
        self.setField("protocol", protocol)
        settings.set_default_selected_protocol(protocol)
        self.completeChanged.emit()
