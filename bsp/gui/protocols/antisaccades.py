from PySide6 import QtWidgets

from bsp.core.protocols import AntisaccadicProtocolTemplate


class AntisaccadicProtocolEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    @property
    def protocol_template(self) -> AntisaccadicProtocolTemplate:
        raise NotImplementedError()
