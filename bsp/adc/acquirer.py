from typing import Callable

from numpy import ndarray, uint16, zeros
from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from .plux import MemoryDev, SignalsDev


class _BSPRecorder(SignalsDev):
    def __init__(self, address: str):
        MemoryDev.__init__(address)
        self.callback: Callable = None

    def set_callback(self, callback: Callable):
        self.callback = callback

    def onRawFrame(self, n_seq: int, data: list):
        return self.callback(n_seq, data)


class BSPAdquirerSignals(QObject):
    available = Signal(ndarray, ndarray)
    finished = Signal()


class BSPAdquirer(QRunnable):
    def __init__(
        self,
        address: str,
        samples: int,
        buffer_length: int = 8,
        parent=None,
    ):
        super().__init__(parent)

        self.signals = BSPAdquirerSignals()

        self._address = address
        self._samples = samples
        self._processed = 0
        self._buffer_length = buffer_length
        self._horizontal = zeros(self._buffer_length, dtype=uint16)
        self._vertical = zeros(self._buffer_length, dtype=uint16)

    def send_data(self, n_seq: int, data: list) -> bool:
        idx = n_seq % self._buffer_length
        self._horizontal[idx] = data[0]
        self._vertical[idx] = data[1]

        if idx == self._buffer_length - 1:
            self.signals.available.emit(
                self._horizontal.copy(),
                self._vertical.copy(),
            )
            self._horizontal *= 0
            self._vertical *= 0

        self._processed += 1
        return self._processed >= self._samples

    @Slot()
    def run(self):
        self._processed = 0
        self._recorder = _BSPRecorder(self._address)
        self._recorder.set_callback(self.send_data)
        self._recorder.start(
            1000,  # Hz
            0x03,  # 2 Channels
            16,  # Bits Resolution
        )
        self._recorder.loop()
        self._recorder.stop()
        self._recorder.close()
        self.signals.finished.emit()
