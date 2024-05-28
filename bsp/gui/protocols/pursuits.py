from PySide6 import QtWidgets

from bsp.core.protocols import PursuitProtocolTemplate


class PursuitProtocolEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    @property
    def protocol_template(self) -> PursuitProtocolTemplate:
        raise NotImplementedError()
