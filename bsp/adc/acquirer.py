import platform
import sys
from os.path import dirname, join
from typing import Callable

from numpy import ndarray, uint16, zeros
from PySide6.QtCore import QObject, QRunnable, Signal, Slot

osDic = {
    "Darwin": f"MacOS/Intel{''.join(platform.python_version().split('.')[:2])}",
    "Linux": "Linux64",
    "Windows": f"Win{platform.architecture()[0][:2]}_{''.join(platform.python_version().split('.')[:2])}",
}
if platform.mac_ver()[0] != "":
    import subprocess
    from os import linesep

    p = subprocess.Popen("sw_vers", stdout=subprocess.PIPE)
    result = p.communicate()[0].decode("utf-8").split(str("\t"))[2].split(linesep)[0]
    if result.startswith("12."):
        print("macOS version is Monterrey!")
        osDic["Darwin"] = "MacOS/Intel310"
        if (
            int(platform.python_version().split(".")[0]) <= 3
            and int(platform.python_version().split(".")[1]) < 10
        ):
            print(
                f"Python version required is ≥ 3.10. Installed is {platform.python_version()}"
            )
            exit()


EXTERNAL_PATH = join(dirname(__file__), f"external/{osDic[platform.system()]}")

sys.path.append(EXTERNAL_PATH)


import plux  # noqa


class _BSPRecorder(plux.SignalsDev):
    def __init__(self, address: str):
        plux.MemoryDev.__init__(address)
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
        self._hor = zeros(self._buffer_length, dtype=uint16)
        self._ver = zeros(self._buffer_length, dtype=uint16)

    def send_data(self, n_seq: int, data: list) -> bool:
        idx = n_seq % self._buffer_length
        self._hor[idx] = data[0]
        self._ver[idx] = data[1]

        if idx == self._buffer_length - 1:
            self.signals.available.emit(
                self._hor.copy(),
                self._ver.copy(),
            )
            self._hor *= 0
            self._ver *= 0

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
