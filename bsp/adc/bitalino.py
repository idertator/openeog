import struct
import time

import serial
from PySide6.QtCore import Slot

from .base import Adquirer

CONTACTING_DEVICE = "The computer lost communication with the device."
DEVICE_NOT_IDLE = "The device is not idle."
DEVICE_NOT_IN_ACQUISITION = "The device is not in acquisition mode."
INVALID_PARAMETER = "Invalid parameter."


class BitalinoRecorder:
    def __init__(self, address):
        self.serial = serial.Serial(address, 115200)
        self.started = False

        print(f"Trying to connect to Bitalino in {address} ...")
        print(self.version())

    def start(self):
        if self.started is False:
            self.send(195)  # 1000 Hz
            self.send(13)  # Setup Analog Channels 0 and 1
            self.started = True
        else:
            raise Exception(DEVICE_NOT_IDLE)

    def stop(self):
        if self.started:
            self.send(0)
        else:
            self.send(255)
        self.started = False

    def close(self):
        self.serial.close()

    def send(self, data):
        time.sleep(0.1)
        self.serial.write(bytes([data]))

    def read(self) -> tuple[int, int]:
        if self.started:
            raw = self.serial.read(4)
            decoded = list(struct.unpack("B B B B ", raw))
            crc = decoded[-1] & 0x0F
            decoded[-1] = decoded[-1] & 0xF0
            x = 0
            for i in range(4):
                for bit in range(7, -1, -1):
                    x = x << 1
                    if x & 0x10:
                        x = x ^ 0x03
                    x = x ^ ((decoded[i] >> bit) & 0x01)
            if crc == x & 0x0F:
                hor = ((decoded[-2] & 0x0F) << 6) | (decoded[-3] >> 2)
                ver = ((decoded[-3] & 0x03) << 8) | decoded[-4]
                return hor, ver
            else:
                raise Exception(CONTACTING_DEVICE)
        else:
            raise Exception(DEVICE_NOT_IN_ACQUISITION)

    def version(self) -> str:
        if self.started is False:
            self.send(7)
            version_str = ""
            while True:
                version_str += self.serial.read(1).decode("utf-8")
                if version_str[-1] == "\n" and "BITalino" in version_str:
                    break
            return version_str[version_str.index("BITalino") : -1]
        else:
            raise Exception(DEVICE_NOT_IDLE)


class BitalinoAdquirer(Adquirer):
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
        self._recorder = BitalinoRecorder(self.address)
        self._recorder.start()

        while self.processed < self.samples:
            hor, ver = self._recorder.read()
            self.send_data(self.processed, [hor, ver])
            time.sleep(0.0005)

        self._recorder.stop()
        self._recorder.close()
        self.signals.finished.emit()
