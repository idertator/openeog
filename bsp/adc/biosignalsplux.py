import platform
import sys
from os.path import dirname, join
from typing import Callable

from PySide6.QtCore import Slot

from .base import Adquirer

EXTERNAL_PATH = join(
    dirname(__file__),
    "external/{platform}_{processor}".format(
        platform=platform.system(),
        processor=platform.processor(),
    ),
)
sys.path.append(EXTERNAL_PATH)

import plux  # noqa


class BiosignalsPluxRecorder(plux.SignalsDev):
    def __init__(self, address: str):
        plux.MemoryDev.__init__(address)
        self.callback: Callable = None

    def set_callback(self, callback: Callable):
        self.callback = callback

    def onRawFrame(self, n_seq: int, data: list):
        return self.callback(n_seq, data)


class BiosignalsPluxAdquirer(Adquirer):
    def __init__(
        self,
        address: str,
        samples: int,
        buffer_length: int = 8,
        parent=None,
    ):
        super().__init__(
            address=address,
            samples=samples,
            buffer_length=buffer_length,
            parent=parent,
        )

    @Slot()
    def run(self):
        self.processed = 0
        self._recorder = BiosignalsPluxRecorder(self.address)
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
