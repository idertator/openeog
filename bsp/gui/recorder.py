from datetime import datetime

from PySide6 import QtCore as qc
from PySide6.QtCore import QObject, Signal

from bsp.adc import BitalinoAcquirer
from bsp.core.logging import log
from bsp.core.models import Session, Study, Test, TestType
from bsp.settings import config

from .plotter import Plotter
from .screens import ScreensManager
from .stimulator import Stimulator


class Recorder(QObject):
    started = Signal()
    stopped = Signal()
    finished = Signal()

    def __init__(
        self,
        screens: ScreensManager,
        stimulator: Stimulator,
        plotter: Plotter,
        parent=None,
    ):
        super().__init__(parent)

        self._screens = screens
        self._stimulator = stimulator
        self._plotter = plotter

        self._acquirer = BitalinoAcquirer(
            address=config.device_address,
            parent=self,
        )
        self._acquirer.available.connect(self.on_samples_available)
        self._acquirer.finished.connect(self.on_adquisition_finished)

        stimulus_screen = config.stimuli_monitor
        refresh_rate = self._screens.refresh_rate(stimulus_screen)
        self._buffer_length = 1000 // refresh_rate

        self._stimulator.started.connect(self.start_test)
        self._stimulator.initialized.connect(self.on_stimulator_initialized)

        self._session: Session | None = None
        self._tests = []
        self._samples_recorded = 0

    def build_study(self) -> Study:
        study = Study(
            recorded_at=datetime.now(),
            tests=[Test(**test) for test in self._tests],
            protocol=self._session.protocol,
        )

        test: Test
        for test in study:
            if test.test_type == TestType.HorizontalSaccadic:
                test.annotate()

        return study

    @property
    def current_hor_position(self) -> int:
        test = self._tests[self._current_test]
        angle = test["angle"] // 2
        stimuli = test["hor_stimuli"]

        if self._samples_recorded < len(stimuli):
            return stimuli[self._samples_recorded] * angle

        return 0

    def start(self, session: Session):
        if not session:
            log.error("No session provided")
            raise ValueError("No session provided")

        self._session = session
        self._tests = session.template.tests
        log.debug(f"{len(self._tests)=}")

        self._current_test = -1
        self._stimulator.open()

        self._acquirer.start(qc.QThread.Priority.TimeCriticalPriority)
        self.started.emit()

    def on_stimulator_initialized(self):
        self.next_test()

    def next_test(self):
        if self._current_test < len(self._tests) - 1:
            self._current_test += 1
            self._samples_recorded = 0

            test = self._tests[self._current_test]
            samples = len(test["hor_stimuli"])
            angle = test["angle"]
            self._acquirer.acquire(samples)

            msg = "{test_type} a {angle}°".format(
                test_type=test["test_type"].name,
                angle=angle,
            )
            log.info(msg)
            self._stimulator.set_message(msg)
        else:
            self._stimulator.close()
            self._acquirer.stop()
            self.finished.emit()

    def start_test(self):
        log.debug("Starting test")
        self._stimulator.set_ball_angle(0, 0)

    def on_samples_available(self, hor, ver):
        samples = len(hor)
        start = self._samples_recorded
        end = start + samples

        test = self._tests[self._current_test]
        stimuli_channel = test["hor_stimuli"]

        total_length = len(stimuli_channel)
        if end <= total_length:
            stimuli = stimuli_channel[start:end]
            test["hor_channel"][start:end] = hor
            test["ver_channel"][start:end] = ver
        else:
            dif = end - total_length
            stimuli = stimuli_channel[start:]
            test["hor_channel"][start:] = hor[:-dif]
            test["ver_channel"][start:] = ver[:-dif]

        stimuli *= 200
        stimuli += 512

        self._samples_recorded += samples
        self._stimulator.set_ball_angle(self.current_hor_position, 0)
        self._plotter.plot_samples(
            hor=hor,
            hor_stimuli=stimuli,
            ver=ver,
            ver_stimulus=stimuli,
        )

    def on_adquisition_finished(self):
        self.next_test()
