from random import randint
from time import time

import numpy as np
from PySide6 import QtCore as qc

from openeog.core.logging import log
from openeog.core.models import Device


class SynthAcquirer(qc.QThread):
    samples_available = qc.Signal(np.ndarray, np.ndarray)
    test_finished = qc.Signal()
    recording_finished = qc.Signal(bool, int)

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(parent)

        self.running = True
        self.samples = 0
        self.stopped = False

    @property
    def device(self) -> Device:
        return Device.Synth

    @property
    def sampling_rate(self) -> int:
        return 1000

    def acquire(self, samples: int):
        self.samples = samples

    def finish(self, stopped: bool = False):
        self.stopped = stopped
        self.running = False

    def run(self):
        buffer_length = 8
        horizontal_channel = np.zeros(buffer_length, dtype=np.uint16)
        vertical_channel = np.zeros(buffer_length, dtype=np.uint16)
        errors = 0

        try:
            while self.running:
                last_time = time() * 1000

                if self.samples:
                    processed = 0

                    while self.running and processed < self.samples:
                        current_time = time() * 1000.0
                        elapsed = current_time - last_time

                        if elapsed < 1.0:
                            continue

                        last_time = current_time

                        hor, ver, ok = randint(0, 1023), randint(0, 1023), True

                        if not ok:
                            errors += 1

                        idx = processed % buffer_length
                        horizontal_channel[idx] = hor
                        vertical_channel[idx] = ver

                        if idx == buffer_length - 1:
                            self.samples_available.emit(
                                horizontal_channel.copy(),
                                vertical_channel.copy(),
                            )
                            horizontal_channel *= 0
                            vertical_channel *= 0

                        processed += 1

                        qc.QThread.sleep(0.00001)

                    self.samples = 0
                    self.test_finished.emit()

                qc.QThread.sleep(0.0005)

        except Exception as err:
            log.error(err)

        finally:
            self.recording_finished.emit(self.stopped, errors)
