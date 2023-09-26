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


class ProtocolsDialog(QDialog):
    def __init__(
        self,
        parent: QWidget = None,
    ):
        super().__init__(parent=parent)
        self.setWindowTitle("Seleccione Protocol")

        self._saccades_protocol_label = QLabel("Protocolo de Sácadas")
        self._saccades_protocol_label.setAlignment(Qt.AlignCenter)
        self._saccades_protocol_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed,
        )

        self._saccades_protocol = QPushButton()
        self._saccades_protocol.setIcon(QIcon(":saccades.svg"))
        self._saccades_protocol.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._saccades_protocol.setFixedSize(250, 100)
        self._saccades_protocol.setIconSize(QSize(250, 100))
        self._saccades_protocol.setCheckable(True)
        self._saccades_protocol.setChecked(True)

        self._pursuit_protocol_label = QLabel("Protocolo de Persecución")
        self._pursuit_protocol_label.setAlignment(Qt.AlignCenter)
        self._pursuit_protocol_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed,
        )

        self._pursuit_protocol = QPushButton()
        self._pursuit_protocol.setIcon(QIcon(":pursuit.svg"))
        self._pursuit_protocol.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._pursuit_protocol.setFixedSize(250, 100)
        self._pursuit_protocol.setIconSize(QSize(250, 100))
        self._pursuit_protocol.setCheckable(True)

        self._buttons = QButtonGroup()
        self._buttons.addButton(self._saccades_protocol)
        self._buttons.addButton(self._pursuit_protocol)

        self._select_button = QPushButton("Seleccionar")
        self._select_button.pressed.connect(self.on_select_pressed)

        self._button_box = QDialogButtonBox(self)
        self._button_box.addButton(
            self._select_button,
            QDialogButtonBox.AcceptRole,
        )

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._saccades_protocol_label)
        self._layout.addWidget(self._saccades_protocol)
        self._layout.addWidget(self._pursuit_protocol_label)
        self._layout.addWidget(self._pursuit_protocol)
        self._layout.addWidget(self._button_box)

        self.setLayout(self._layout)

    @property
    def protocol(self) -> Protocol:
        if self._pursuit_protocol.isChecked():
            return Protocol.Pursuit
        return Protocol.Saccadic

    @Slot()
    def on_select_pressed(self):
        self.close()
