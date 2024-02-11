from numpy import ndarray, uint16, zeros
from PySide6.QtCore import QObject, QRunnable, Signal


class AdquirerSignals(QObject):
    available = Signal(ndarray, ndarray)
    finished = Signal()


class Adquirer(QRunnable):
    def __init__(
        self,
        address: str,
        samples: int,
        buffer_length: int = 8,
        parent=None,
    ):
        super().__init__(parent)

        self.signals = AdquirerSignals()

        self.address = address
        self.samples = samples
        self.processed = 0
        self.buffer_length = buffer_length
        self.horizontal_channel = zeros(self.buffer_length, dtype=uint16)
        self.vertical_channel = zeros(self.buffer_length, dtype=uint16)

    def send_data(self, n_seq: int, data: list) -> bool:
        idx = n_seq % self.buffer_length
        self.horizontal_channel[idx] = data[0]
        self.vertical_channel[idx] = data[1]

        if idx == self.buffer_length - 1:
            self.signals.available.emit(
                self.horizontal_channel.copy(),
                self.vertical_channel.copy(),
            )
            self.horizontal_channel *= 0
            self.vertical_channel *= 0

        self.processed += 1
        return self.processed >= self.samples
