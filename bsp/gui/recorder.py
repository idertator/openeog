from datetime import datetime
from typing import Type

from numpy import uint16, zeros
from PySide6.QtCore import QObject, QThreadPool, Signal

from bsp.adc import Adquirer, BiosignalsPluxAdquirer, BitalinoAdquirer
from bsp.core import Protocol, Study, Test, TestType, pursuit_stimuli, saccadic_stimuli

from .plotter import Plotter
from .protocols import PROTOCOLS
from .screens import ScreensManager
from .settings import SettingsDialog
from .stimulator import Stimulator


class Recorder(QObject):
    CALIBRATION_SACCADES = 10
    CALIBRATION_SAMPLES = 20000

    SACCADIC_SAMPLES = 40000
    SACCADES_COUNT = 20

    PURSUIT_SAMPLES = 40000
    PURSUIT_VELOCITY = 1.5

    started = Signal()
    stopped = Signal()
    finished = Signal()

    def __init__(
        self,
        screens: ScreensManager,
        settings: SettingsDialog,
        stimulator: Stimulator,
        plotter: Plotter,
        parent=None,
    ):
        super().__init__(parent)

        self._threadpool = QThreadPool()
        self._screens = screens
        self._settings = settings
        self._stimulator = stimulator
        self._plotter = plotter
        self._adquirer = None

        stimulus_screen = self._settings.stimuli_monitor
        refresh_rate = self._screens.refresh_rate(stimulus_screen)
        self._buffer_length = 1000 // refresh_rate

        self._stimulator.started.connect(self.start_test)
        self._stimulator.initialized.connect(self.on_stimulator_initialized)

        self._tests = []
        self._samples_recorded = 0
        self._protocol = PROTOCOLS[0]["protocol"]

    def build_study(self) -> Study:
        study = Study(
            recorded_at=datetime.now(),
            tests=[Test(**test) for test in self._tests],
            protocol=self._protocol,
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

    @property
    def protocol(self) -> Protocol:
        return self._protocol

    @protocol.setter
    def protocol(self, protocol: Protocol):
        self._protocol = protocol

    def initialize_saccadic_protocol(self):
        self._tests = [
            {
                "test_type": TestType.HorizontalCalibration,
                "angle": 30,
                "hor_stimuli": saccadic_stimuli(
                    length=self.CALIBRATION_SAMPLES,
                    saccades=self.CALIBRATION_SACCADES,
                ),
                "hor_channel": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
                "ver_stimuli": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
                "ver_channel": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
            },
            {
                "test_type": TestType.HorizontalSaccadic,
                "angle": 10,
                "hor_stimuli": saccadic_stimuli(
                    length=self.SACCADIC_SAMPLES,
                    saccades=self.SACCADES_COUNT,
                ),
                "hor_channel": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
                "ver_stimuli": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
                "ver_channel": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
            },
            {
                "test_type": TestType.HorizontalSaccadic,
                "angle": 20,
                "hor_stimuli": saccadic_stimuli(
                    length=self.SACCADIC_SAMPLES,
                    saccades=self.SACCADES_COUNT,
                ),
                "hor_channel": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
                "ver_stimuli": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
                "ver_channel": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
            },
            {
                "test_type": TestType.HorizontalSaccadic,
                "angle": 30,
                "hor_stimuli": saccadic_stimuli(
                    length=self.SACCADIC_SAMPLES,
                    saccades=self.SACCADES_COUNT,
                ),
                "hor_channel": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
                "ver_stimuli": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
                "ver_channel": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
            },
            {
                "test_type": TestType.HorizontalSaccadic,
                "angle": 60,
                "hor_stimuli": saccadic_stimuli(
                    length=self.SACCADIC_SAMPLES,
                    saccades=self.SACCADES_COUNT,
                ),
                "hor_channel": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
                "ver_stimuli": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
                "ver_channel": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
            },
            {
                "test_type": TestType.HorizontalCalibration,
                "angle": 30,
                "hor_stimuli": saccadic_stimuli(
                    length=self.CALIBRATION_SAMPLES,
                    saccades=self.CALIBRATION_SACCADES,
                ),
                "hor_channel": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
                "ver_stimuli": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
                "ver_channel": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
            },
        ]

    def initialize_antisaccadic_protocol(self):
        self._tests = [
            {
                "test_type": TestType.HorizontalCalibration,
                "angle": 30,
                "hor_stimuli": saccadic_stimuli(
                    length=self.CALIBRATION_SAMPLES,
                    saccades=self.CALIBRATION_SACCADES,
                ),
                "hor_channel": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
                "ver_stimuli": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
                "ver_channel": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
            },
            {
                "test_type": TestType.HorizontalAntisaccadic,
                "angle": 30,
                "hor_stimuli": saccadic_stimuli(
                    length=self.SACCADIC_SAMPLES,
                    saccades=self.SACCADES_COUNT,
                ),
                "hor_channel": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
                "ver_stimuli": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
                "ver_channel": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
            },
            {
                "test_type": TestType.HorizontalCalibration,
                "angle": 30,
                "hor_stimuli": saccadic_stimuli(
                    length=self.CALIBRATION_SAMPLES,
                    saccades=self.CALIBRATION_SACCADES,
                ),
                "hor_channel": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
                "ver_stimuli": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
                "ver_channel": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
            },
        ]

    def initialize_pursuit_protocol(self):
        self._tests = [
            {
                "test_type": TestType.HorizontalCalibration,
                "angle": 30,
                "hor_stimuli": saccadic_stimuli(
                    length=self.CALIBRATION_SAMPLES,
                    saccades=self.CALIBRATION_SACCADES,
                ),
                "hor_channel": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
                "ver_stimuli": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
                "ver_channel": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
            },
            {
                "test_type": TestType.HorizontalPursuit,
                "angle": 30,
                "hor_stimuli": pursuit_stimuli(
                    length=self.PURSUIT_SAMPLES,
                    speed=self.PURSUIT_VELOCITY,
                ),
                "hor_channel": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
                "ver_stimuli": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
                "ver_channel": zeros(self.SACCADIC_SAMPLES, dtype=uint16),
            },
            {
                "test_type": TestType.HorizontalCalibration,
                "angle": 30,
                "hor_stimuli": saccadic_stimuli(
                    length=self.CALIBRATION_SAMPLES,
                    saccades=self.CALIBRATION_SACCADES,
                ),
                "hor_channel": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
                "ver_stimuli": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
                "ver_channel": zeros(self.CALIBRATION_SAMPLES, dtype=uint16),
            },
        ]

    def start(self):
        if self._protocol == Protocol.Saccadic:
            self.initialize_saccadic_protocol()
        elif self._protocol == Protocol.Antisaccadic:
            self.initialize_antisaccadic_protocol()
        elif self._protocol == Protocol.Pursuit:
            self.initialize_pursuit_protocol()
        else:
            raise Exception("Invalid protocol")

        self._current_test = -1
        self._stimulator.open()

        self.started.emit()

    def on_stimulator_initialized(self):
        self.next_test()

    @property
    def acquirer_class(self) -> Type[Adquirer]:
        if self._settings.device_type == "Bitalino":
            return BitalinoAdquirer

        return BiosignalsPluxAdquirer

    def next_test(self):
        if self._current_test < len(self._tests) - 1:
            self._current_test += 1
            self._samples_recorded = 0

            test = self._tests[self._current_test]
            samples = len(test["hor_stimuli"])
            angle = test["angle"]

            self._adquirer = self.acquirer_class(
                address=self._settings.device_address,
                samples=samples,
                buffer_length=self._buffer_length,
                parent=self,
            )
            self._adquirer.signals.available.connect(self.on_samples_available)
            self._adquirer.signals.finished.connect(self.on_adquisition_finished)

            self._stimulator.set_message(
                "{test_type} a {angle}°".format(
                    test_type=test["test_type"].name,
                    angle=angle,
                ),
            )
        else:
            self._stimulator.close()
            self.finished.emit()

    def start_test(self):
        self._stimulator.set_ball_angle(0, 0)
        self._threadpool.start(self._adquirer)

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
        self._adquirer.signals.available.disconnect(self.on_samples_available)
        self._adquirer.signals.finished.disconnect(self.on_adquisition_finished)
        self._adquirer = None
        self.next_test()
