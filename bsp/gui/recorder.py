from datetime import datetime

import numpy as np
from PySide6 import QtCore as qc

from bsp.adc import BitalinoAcquirer, SynthAcquirer
from bsp.core.logging import log
from bsp.core.models import Conditions, Hardware, Protocol, Session, Study, Test
from bsp.settings import config

from .plotter import Plotter
from .screens import ScreensManager
from .stimulator import Stimulator


class Recorder(qc.QObject):
    started = qc.Signal()
    stopped = qc.Signal()
    finished = qc.Signal()

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

        match config.device_type:
            case "Bitalino":
                self._acquirer: BitalinoAcquirer = BitalinoAcquirer(
                    address=config.device_address,
                    parent=self,
                )

            case "Synth":
                self._acquirer: SynthAcquirer = SynthAcquirer()

            case _:
                raise ValueError(f"Unsupported device: {config.device_type}")

        self._acquirer.samples_available.connect(self.on_samples_available)
        self._acquirer.test_finished.connect(self.on_test_finished)
        self._acquirer.recording_finished.connect(self.on_recording_finished)

        stimulus_screen = config.stimuli_monitor
        refresh_rate = self._screens.refresh_rate(stimulus_screen)
        self._buffer_length = 1000 // refresh_rate

        self._stimulator.started.connect(self.start_test)
        self._stimulator.initialized.connect(self.on_stimulator_initialized)

        self._session: Session | None = None
        self._tests = []
        self._samples_recorded = 0
        self._already_finished = False
        self._errors = 0

    @property
    def protocol(self) -> Protocol:
        return self._session.protocol

    @property
    def hardware(self) -> Hardware:
        stimuli_monitor = config.stimuli_monitor
        stimuli_screen_size = self._screens.screen_size(stimuli_monitor)
        return Hardware(
            acquisition_device=self._acquirer.device,
            acquisition_sampling_rate=self._acquirer.sampling_rate,
            stimuli_monitor=stimuli_monitor,
            stimuli_monitor_refresh_rate=self._screens.refresh_rate(stimuli_monitor),
            stimuli_monitor_width=config.stimuli_monitor_width,
            stimuli_monitor_height=config.stimuli_monitor_height,
            stimuli_monitor_resolution_width=stimuli_screen_size.width(),
            stimuli_monitor_resolution_height=stimuli_screen_size.height(),
            stimuli_ball_radius=config.stimuli_ball_radius,
        )

    @property
    def conditions(self) -> Conditions:
        return Conditions(
            light_intensity=self._session.light_intensity,
            errors=self._errors,
        )

    def build_study(self) -> Study:
        return Study(
            recorded_at=datetime.now(),
            protocol=self.protocol,
            tests=[Test(**test) for test in self._tests],
            hardware=self.hardware,
            conditions=self.conditions,
        )

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
            log.error("no session provided")
            raise ValueError("no session provided")

        self._session = session
        self._tests = session.template.tests

        self._current_test = -1
        self._stimulator.open()

        self._acquirer.start()
        self.started.emit()

    def stop(self):
        if self._acquirer:
            self._acquirer.finish(stopped=True)
            self.stopped.emit()

    def on_stimulator_initialized(self):
        self.next_test()

    def next_test(self):
        if self._current_test < len(self._tests) - 1:
            self._current_test += 1
            self._samples_recorded = 0

            test = self._tests[self._current_test]
            angle = test["angle"]

            if test.get("replica", False):
                msg = "{test_type} a {angle}° (Replica)".format(
                    test_type=test["test_type"].name,
                    angle=angle,
                )
            else:
                msg = "{test_type} a {angle}°".format(
                    test_type=test["test_type"].name,
                    angle=angle,
                )

            log.info(msg)
            self._stimulator.set_message(msg)
        else:
            self._acquirer.finish(stopped=False)

    def start_test(self):
        self._stimulator.set_ball_angle(0, 0)

        test = self._tests[self._current_test]
        samples = len(test["hor_stimuli"])
        self._acquirer.acquire(samples)

    def on_samples_available(
        self,
        hor: np.ndarray,
        ver: np.ndarray,
    ):
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

    def on_test_finished(self):
        self.next_test()

    def on_recording_finished(self, stopped: bool, errors: int):
        self._errors = errors
        if not self._already_finished:
            self._already_finished = True
            self._stimulator.close()
            self._acquirer.finish()

            if not stopped:
                self.finished.emit()
