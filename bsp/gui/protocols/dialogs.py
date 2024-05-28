from PySide6.QtCore import QSize, Qt, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from bsp.core import Protocol
from bsp.gui.config import PROTOCOLS


class ProtocolsDialog(QDialog):
    def __init__(
        self,
        parent: QWidget = None,
    ):
        super().__init__(parent=parent)
        self.setWindowTitle("Seleccione Protocol")

        self._layout = QVBoxLayout()
        self._buttons_group = QButtonGroup()
        self._protocols = {}

        for idx, protocol in enumerate(PROTOCOLS):
            label = QLabel(protocol["name"])
            label.setAlignment(Qt.AlignCenter)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            button = QPushButton()
            button.setIcon(QIcon(protocol["icon"]))
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            button.setFixedSize(250, 100)
            button.setIconSize(QSize(250, 100))
            button.setCheckable(True)

            if idx == 0:
                button.setChecked(True)

            self._buttons_group.addButton(button)
            self._layout.addWidget(label)
            self._layout.addWidget(button)

            self._protocols[id(button)] = protocol["protocol"]

        self._select_button = QPushButton("Seleccionar")
        self._select_button.pressed.connect(self.on_select_pressed)

        self._button_box = QDialogButtonBox(self)
        self._button_box.addButton(
            self._select_button,
            QDialogButtonBox.AcceptRole,
        )

        self._layout.addWidget(self._button_box)

        self.setLayout(self._layout)

    @property
    def protocol(self) -> Protocol:
        for button in self._buttons_group.buttons():
            if button.isChecked():
                protocol = self._protocols[id(button)]
                return protocol

        raise ValueError("No protocol selected")

    @Slot()
    def on_select_pressed(self):
        self.close()
