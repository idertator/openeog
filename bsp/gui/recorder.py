from datetime import datetime

from numpy import uint16, zeros
from PySide6.QtCore import QObject, QThreadPool, Signal

from bsp.adc import BSPAdquirer
from bsp.core.models import Study, Test, TestType
from bsp.core.stimuli import horizontal_saccadic_stimulus

from .plotter import Plotter
from .screens import ScreensManager
from .settings import SettingsDialog
from .stimulator import Stimulator


class Recorder(QObject):
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
        self._buffer_length = (1000 // refresh_rate) >> 1

        self._stimulator.started.connect(self.start_test)
        self._stimulator.initialized.connect(self.on_stimulator_initialized)

        self._tests = []
        self._samples_recorded = 0

    def build_study(self) -> Study:
        return Study(
            datetime.now(),
            *[Test(**test) for test in self._tests],
        )

    @property
    def current_horizontal_position(self) -> int:
        test = self._tests[self._current_test]
        angle = test["angle"] // 2
        stimuli = test["horizontal_stimuli"]

        if self._samples_recorded < len(stimuli):
            return stimuli[self._samples_recorded] * angle

        return 0

    def start(self):
        self._tests = [
            {
                "test_type": TestType.HorizontalCalibration,
                "angle": 30,
                "horizontal_stimuli": horizontal_saccadic_stimulus(
                    length=20000,
                    saccades=10,
                ),
                "horizontal_channel": zeros(30000, dtype=uint16),
                "vertical_stimuli": zeros(30000, dtype=uint16),
                "vertical_channel": zeros(30000, dtype=uint16),
            },
            {
                "test_type": TestType.HorizontalSaccadicTest,
                "angle": 10,
                "horizontal_stimuli": horizontal_saccadic_stimulus(
                    length=40000,
                    saccades=20,
                ),
                "horizontal_channel": zeros(60000, dtype=uint16),
                "vertical_stimuli": zeros(60000, dtype=uint16),
                "vertical_channel": zeros(60000, dtype=uint16),
            },
            {
                "test_type": TestType.HorizontalSaccadicTest,
                "angle": 20,
                "horizontal_stimuli": horizontal_saccadic_stimulus(
                    length=40000,
                    saccades=20,
                ),
                "horizontal_channel": zeros(60000, dtype=uint16),
                "vertical_stimuli": zeros(60000, dtype=uint16),
                "vertical_channel": zeros(60000, dtype=uint16),
            },
            {
                "test_type": TestType.HorizontalSaccadicTest,
                "angle": 30,
                "horizontal_stimuli": horizontal_saccadic_stimulus(
                    length=40000,
                    saccades=20,
                ),
                "horizontal_channel": zeros(60000, dtype=uint16),
                "vertical_stimuli": zeros(60000, dtype=uint16),
                "vertical_channel": zeros(60000, dtype=uint16),
            },
            {
                "test_type": TestType.HorizontalSaccadicTest,
                "angle": 60,
                "horizontal_stimuli": horizontal_saccadic_stimulus(
                    length=40000,
                    saccades=20,
                ),
                "horizontal_channel": zeros(60000, dtype=uint16),
                "vertical_stimuli": zeros(60000, dtype=uint16),
                "vertical_channel": zeros(60000, dtype=uint16),
            },
            {
                "test_type": TestType.HorizontalCalibration,
                "angle": 30,
                "horizontal_stimuli": horizontal_saccadic_stimulus(
                    length=20000,
                    saccades=10,
                ),
                "horizontal_channel": zeros(30000, dtype=uint16),
                "vertical_stimuli": zeros(30000, dtype=uint16),
                "vertical_channel": zeros(30000, dtype=uint16),
            },
        ]
        self._current_test = -1
        self._stimulator.open()

        self.started.emit()

    def on_stimulator_initialized(self):
        self.next_test()

    def next_test(self):
        if self._current_test < len(self._tests) - 1:
            self._current_test += 1
            self._samples_recorded = 0

            test = self._tests[self._current_test]
            samples = len(test["horizontal_stimuli"])
            angle = test["angle"]

            self._adquirer = BSPAdquirer(
                address=self._settings.device_address,
                samples=samples,
                buffer_length=self._buffer_length,
                parent=self,
            )
            self._adquirer.signals.available.connect(self.on_samples_available)
            self._adquirer.signals.finished.connect(self.on_adquisition_finished)

            self._stimulator.set_message(
                "{test_type} at {angle}°".format(
                    test_type=test["test_type"],
                    angle=angle,
                ),
            )
        else:
            self._stimulator.close()
            self.finished.emit()

    def start_test(self):
        self._stimulator.set_ball_angle(0, 0)
        self._threadpool.start(self._adquirer)

    def on_samples_available(self, horizontal, vertical):
        samples = len(horizontal)
        start = self._samples_recorded
        end = start + samples

        test = self._tests[self._current_test]
        stimuli_channel = test["horizontal_stimuli"]

        total_length = len(stimuli_channel)
        if end <= total_length:
            stimuli = stimuli_channel[start:end]
            test["horizontal_channel"][start:end] = horizontal
            test["vertical_channel"][start:end] = vertical
        else:
            dif = end - total_length
            stimuli = stimuli_channel[start:]
            test["horizontal_channel"][start:] = horizontal[:-dif]
            test["vertical_channel"][start:] = vertical[:-dif]

        stimuli *= 20000
        stimuli += 32768

        self._samples_recorded += samples
        self._stimulator.set_ball_angle(self.current_horizontal_position, 0)
        self._plotter.plot_samples(
            horizontal=horizontal,
            horizontal_stimulus=stimuli,
            vertical=vertical,
            vertical_stimulus=stimuli,
        )

    def on_adquisition_finished(self):
        self._adquirer.signals.available.disconnect(self.on_samples_available)
        self._adquirer.signals.finished.disconnect(self.on_adquisition_finished)
        self._adquirer = None
        self.next_test()
