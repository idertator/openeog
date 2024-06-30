from __future__ import annotations

import struct
import time

import numpy as np
import serial
from PySide6 import QtCore as qc

from bsp.core.logging import log

CONTACTING_DEVICE = "The computer lost communication with the device."
DEVICE_NOT_IDLE = "The device is not idle."
DEVICE_NOT_IN_ACQUISITION = "The device is not in acquisition mode."
INVALID_PARAMETER = "Invalid parameter."


class BitalinoSerialRecorder:
    _instance: BitalinoSerialRecorder = None

    def __init__(self, address: str):
        self.address = address
        self.initialized = False
        self.started = False
        self.serial: serial.Serial | None = None

    @classmethod
    def instance(cls, address: str) -> BitalinoSerialRecorder:
        if cls._instance is None:
            cls._instance = BitalinoSerialRecorder(address)
        return cls._instance

    def connect(self):
        log.info(f"connecting to Bitalino through '{self.address}'")

        if not self.serial:
            self.serial = serial.Serial(self.address, 115200)

        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()

        if not self.initialized:
            log.info(f"trying to connect to Bitalino in {self.address} ...")
            version = self.get_version()
            log.info(f"connected to {version}")
            self.initialized = True

    def start(self):
        log.debug("starting acquisition")
        self.connect()

        if not self.started:
            self.send_command(195)  # 1000 Hz
            self.send_command(13)  # Setup Analog Channels 0 and 1
            self.started = True
        else:
            log.error(DEVICE_NOT_IDLE)
            raise Exception(DEVICE_NOT_IDLE)

    def stop(self):
        log.debug("stopping acquisition")
        if self.started:
            self.send_command(0)
        else:
            self.send_command(255)
        self.started = False

    def close(self):
        log.info("closing Bitalino")
        self.stop()
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()
        self.serial.close()
        self.serial = None

    def send_command(self, data: int):
        time.sleep(0.1)
        self.serial.write(bytes([data]))

    def read_data(self) -> tuple[int, int]:
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

            hor = ((decoded[-2] & 0x0F) << 6) | (decoded[-3] >> 2)
            ver = ((decoded[-3] & 0x03) << 8) | decoded[-4]

            if crc != (x & 0x0F):
                log.debug("Wrong packet CRC")

            return hor, ver
        else:
            log.error(DEVICE_NOT_IN_ACQUISITION)
            raise Exception(DEVICE_NOT_IN_ACQUISITION)

    def get_version(self) -> str:
        if not self.started:
            self.send_command(7)
            version_str = ""
            while True:
                version_str += self.serial.read(1).decode("utf-8")
                if version_str[-1] == "\n" and "BITalino" in version_str:
                    break
            return version_str[version_str.index("BITalino") : -1]
        else:
            raise Exception(DEVICE_NOT_IDLE)


class BitalinoAcquirer(qc.QThread):
    available = qc.Signal(np.ndarray, np.ndarray)
    finished = qc.Signal()

    def __init__(
        self,
        address: str,
        samples: int,
        buffer_length: int = 8,
        parent=None,
    ):
        super().__init__(parent)

        self.address = address
        self.samples = samples
        self.processed = 0
        self.buffer_length = buffer_length
        self.horizontal_channel = np.zeros(self.buffer_length, dtype=np.uint16)
        self.vertical_channel = np.zeros(self.buffer_length, dtype=np.uint16)

    def send_data(self, n_seq: int, data: list) -> bool:
        idx = n_seq % self.buffer_length
        self.horizontal_channel[idx] = data[0]
        self.vertical_channel[idx] = data[1]

        if idx == self.buffer_length - 1:
            self.available.emit(
                self.horizontal_channel.copy(),
                self.vertical_channel.copy(),
            )
            self.horizontal_channel *= 0
            self.vertical_channel *= 0

        self.processed += 1
        return self.processed >= self.samples

    def run(self):
        try:
            recorder = BitalinoSerialRecorder.instance(self.address)

            self.processed = 0
            recorder.start()

            while self.processed < self.samples:
                hor, ver = recorder.read_data()
                self.send_data(self.processed, [hor, ver])
                time.sleep(0.001)

        except Exception as err:
            log.error(err)

        finally:
            recorder.stop()
            recorder.close()

            self.finished.emit()
