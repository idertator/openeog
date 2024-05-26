from __future__ import annotations

from datetime import datetime
from enum import Enum
from functools import cached_property

from numpy import ndarray, single

from .calibration import calibration
from .denoising import denoise
from .saccades import saccades


class Direction(str, Enum):
    Same = "same"
    Left = "left"
    Right = "right"


class Size(str, Enum):
    Invalid = "inv"
    Small = "small"
    Large = "large"


class Protocol(str, Enum):
    Saccadic = "saccadic"
    Pursuit = "pursuit"
    Antisaccadic = "antisaccadic"

    @property
    def name(self) -> str:
        match self:
            case Protocol.Saccadic:
                return "Protocolo Sacádico"

            case Protocol.Pursuit:
                return "Protocolo de Persecución"

            case Protocol.Antisaccadic:
                return "Protocolo Antisacádico"


class TestType(str, Enum):
    HorizontalCalibration = "HorizontalCalibration"
    HorizontalSaccadic = "HorizontalSaccadic"
    VerticalCalibration = "VerticalCalibration"
    HorizontalPursuit = "HorizontalPursuit"
    HorizontalAntisaccadic = "HorizontalAntisaccadic"
    VerticalAntisaccadic = "VerticalAntisaccadic"

    @property
    def name(self) -> str:
        match self:
            case TestType.HorizontalCalibration:
                return "Calibración Horizontal"

            case TestType.HorizontalSaccadic:
                return "Sacádica"

            case TestType.VerticalCalibration:
                return "Calibración Vertical"

            case TestType.HorizontalPursuit:
                return "Persecución Horizontal"

            case TestType.HorizontalAntisaccadic:
                return "Antisacádica Horizontal"

            case TestType.VerticalAntisaccadic:
                return "Antisacádica Vertical"

        return "Desconocida"


class AnnotationType(str, Enum):
    Fixation = "Fixation"
    Saccade = "Saccade"
    Pursuit = "Pursuit"
    AntiSaccade = "AntiSaccade"

    @property
    def name(self) -> str:
        match self:
            case AnnotationType.Fixation:
                return "Fijación"

            case AnnotationType.Saccade:
                return "Sácada"

            case AnnotationType.Pursuit:
                return "Persecución"

            case AnnotationType.AntiSaccade:
                return "AntiSaccade"

        return "Desconocida"


class Annotation:
    def __init__(
        self,
        annotation_type: AnnotationType,
        onset: int,
        offset: int,
    ):
        self._annotation_type = annotation_type
        self.onset = onset
        self.offset = offset

    def __str__(self):
        return "{annotation} from {onset} to {offset}".format(
            annotation=self._annotation_type.value,
            onset=self.onset,
            offset=self.offset,
        )

    @property
    def json(self) -> dict:
        return {
            "annotation_type": self._annotation_type.value,
            "onset": self.onset,
            "offset": self.offset,
        }

    @property
    def annotation_type(self) -> AnnotationType:
        return self._annotation_type


class Saccade(Annotation):
    def __init__(
        self,
        onset: int,
        offset: int,
        latency: int = 0,
        duration: int = 0,
        amplitude: float = 0.0,
        deviation: float = 0.0,
        peak_velocity: float = 0.0,
        transition_index: int = -1,
        transition_change_index: int = -1,
        transition_change_before_index: int = -1,
        transition_direction: Direction = Direction.Same,
        direction: Direction = Direction.Same,
        size: Size = Size.Invalid,
    ):
        super().__init__(
            annotation_type=AnnotationType.Saccade,
            onset=onset,
            offset=offset,
        )
        self.direction = direction
        self.size = size
        self.latency = latency
        self.duration = duration
        self.amplitude = amplitude
        self.deviation = deviation
        self.peak_velocity = peak_velocity
        self.transition_index = transition_index
        self.transition_change_index = transition_change_index
        self.transition_change_before_index = transition_change_before_index
        self.transition_direction = transition_direction

    @property
    def json(self) -> dict:
        return {
            **super().json,
            "direction": self.direction.value,
            "size": self.size.value,
            "latency": self.latency,
            "duration": self.duration,
            "amplitude": self.amplitude,
            "deviation": self.deviation,
            "peak_velocity": self.peak_velocity,
            "transition_index": self.transition_index,
            "transition_change_index": self.transition_change_index,
            "transition_change_before_index": self.transition_change_before_index,
            "transition_direction": self.transition_direction.value,
        }


class AntiSaccade(Annotation):
    def __init__(
        self,
        onset: int,
        offset: int,
        latency: int = 0,
        duration: int = 0,
        amplitude: float = 0.0,
        deviation: float = 0.0,
        peak_velocity: float = 0.0,
        transition_index: int = -1,
        transition_change_index: int = -1,
        transition_change_before_index: int = -1,
        transition_direction: Direction = Direction.Same,
        direction: Direction = Direction.Same,
        size: Size = Size.Invalid,
    ):
        super().__init__(
            annotation_type=AnnotationType.AntiSaccade,
            onset=onset,
            offset=offset,
        )
        self.direction = direction
        self.size = size
        self.latency = latency
        self.duration = duration
        self.amplitude = amplitude
        self.deviation = deviation
        self.peak_velocity = peak_velocity
        self.transition_index = transition_index
        self.transition_change_index = transition_change_index
        self.transition_change_before_index = transition_change_before_index
        self.transition_direction = transition_direction

    @property
    def json(self) -> dict:
        return {
            **super().json,
            "direction": self.direction.value,
            "size": self.size.value,
            "latency": self.latency,
            "duration": self.duration,
            "amplitude": self.amplitude,
            "deviation": self.deviation,
            "peak_velocity": self.peak_velocity,
            "transition_index": self.transition_index,
            "transition_change_index": self.transition_change_index,
            "transition_change_before_index": self.transition_change_before_index,
            "transition_direction": self.transition_direction.value,
        }


class Test:
    def __init__(
        self,
        test_type: TestType,
        angle: int,
        hor_stimuli: ndarray,
        hor_channel: ndarray,
        ver_stimuli: ndarray,
        ver_channel: ndarray,
        hor_annotations: list[Annotation] = [],
        ver_annotations: list[Annotation] = [],
        fs: int = 1000,
        **kwargs,
    ):
        self._test_type = test_type
        self._angle = angle
        self._fs = fs

        self._hor_stimuli = hor_stimuli
        self._hor_channel = hor_channel
        self._ver_stimuli = ver_stimuli
        self._ver_channel = ver_channel
        self._hor_annotations = hor_annotations
        self._ver_annotations = ver_annotations

        self._hor_calibration: float = 1.0
        self._ver_calibration: float = 1.0

    def __str__(self):
        return "{test} at {angle}°".format(
            test=self._test_type.value,
            angle=self._angle,
        )

    @property
    def json(self) -> dict:
        return {
            "test_type": self._test_type.value,
            "angle": self._angle,
            "fs": self._fs,
            "length": len(self.hor_stimuli),
            "hor_annotations": [a.json for a in self._hor_annotations],
            "ver_annotations": [a.json for a in self._ver_annotations],
        }

    @property
    def test_type(self) -> TestType:
        return self._test_type

    @property
    def angle(self) -> int:
        return self._angle

    @property
    def fs(self) -> int:
        return self._fs

    @cached_property
    def hor_stimuli(self) -> ndarray:
        normalized = (self._hor_stimuli - 32768) / 20000
        scaled = normalized.astype(single) * (self.angle / 2)
        return scaled

    @property
    def hor_stimuli_raw(self) -> ndarray:
        return self._hor_stimuli

    @cached_property
    def hor_channel(self) -> ndarray:
        scaled = self._hor_channel.astype(single) * self._hor_calibration
        centered = scaled - scaled.mean()
        return denoise(centered)

    @property
    def hor_channel_raw(self) -> ndarray:
        return self._hor_channel

    @cached_property
    def ver_stimuli(self) -> ndarray:
        normalized = (self._ver_stimuli - 32768) / 20000
        scaled = normalized.astype(single) * (self.angle / 2)
        return scaled

    @property
    def ver_stimuli_raw(self) -> ndarray:
        return self._ver_stimuli

    @cached_property
    def ver_channel(self) -> ndarray:
        scaled = self._ver_channel.astype(single) * self._hor_calibration
        centered = scaled - scaled.mean()
        return denoise(centered)

    @property
    def ver_channel_raw(self) -> ndarray:
        return self._ver_channel

    @property
    def hor_annotations(self) -> list[Annotation]:
        return self._hor_annotations

    @property
    def hor_saccades(self) -> list[Saccade]:
        return [a for a in self._hor_annotations if isinstance(a, Saccade)]

    @property
    def ver_annotations(self) -> list[Annotation]:
        return self._ver_annotations

    @property
    def hor_calibration(self) -> float:
        return self._hor_calibration

    @hor_calibration.setter
    def hor_calibration(self, value: float):
        self._hor_calibration = value or 1.0

    @property
    def ver_calibration(self) -> float:
        return self._ver_calibration

    @ver_calibration.setter
    def ver_calibration(self, value: float):
        self._ver_calibration = value or 1.0

    def annotate(self):
        """Identify annotations"""

        if self.test_type == TestType.HorizontalSaccadic:
            result = []

            for onset, offset in saccades(
                channel=self.hor_channel,
                angle=self.angle,
            ):
                result.append(
                    Saccade(
                        onset=onset,
                        offset=offset,
                    )
                )

            self._hor_annotations = result


class Study:
    VERSION = "1.0"

    def __init__(
        self,
        recorded_at: datetime | None,
        tests: list[Test],
        protocol: Protocol,
        hor_calibration: float | None = None,
        hor_calibration_diff: float | None = None,
        ver_calibration: float | None = None,
        ver_calibration_diff: float | None = None,
        **kwargs,
    ):
        self._recorded_at = recorded_at or datetime.now()

        if hor_calibration is None:
            initial_calibration = None
            final_calibration = None
            for test in tests:
                if test.test_type == TestType.HorizontalCalibration:
                    if initial_calibration is None:
                        initial_calibration = test
                    final_calibration = test

            if initial_calibration and final_calibration:
                assert initial_calibration.angle == final_calibration.angle

            hor_calibration, hor_calibration_diff = calibration(
                initial=initial_calibration.hor_channel,
                final=final_calibration.hor_channel,
                angle=initial_calibration.angle,
            )

        self._hor_calibration = hor_calibration or 1.0
        self._hor_calibration_diff = hor_calibration_diff

        if ver_calibration is None:
            initial_calibration = None
            final_calibration = None
            for test in tests:
                if test.test_type == TestType.VerticalCalibration:
                    if initial_calibration is None:
                        initial_calibration = test
                    final_calibration = test

            if initial_calibration and final_calibration:
                assert initial_calibration.angle == final_calibration.angle

                ver_calibration, ver_calibration_diff = calibration(
                    initial=initial_calibration.ver_channel,
                    final=final_calibration.ver_channel,
                    angle=initial_calibration.angle,
                )

        self._ver_calibration = ver_calibration or 1.0
        self._ver_calibration_diff = ver_calibration_diff

        for test in tests:
            test.hor_calibration = self._hor_calibration or 1.0

        self._tests = tests
        self._protocol = protocol

    def __str__(self) -> str:
        return "Study recorded at {recorded_at} with {num_tests} tests".format(
            recorded_at=self._recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
            num_tests=len(self._tests),
        )

    def __len__(self) -> int:
        return len(self._tests)

    def __getitem__(self, index: int) -> Test:
        return self._tests[index]

    @property
    def json(self) -> dict:
        return {
            "version": self.VERSION,
            "recorded_at": self._recorded_at.timestamp(),
            "tests": [test.json for test in self._tests],
            "hor_calibration": float(self._hor_calibration or 1.0),
            "hor_calibration_diff": float(self._hor_calibration_diff or 1.0),
            "ver_calibration": float(self._ver_calibration or 1.0),
            "ver_calibration_diff": float(self._ver_calibration_diff or 1.0),
            "protocol": self._protocol.value,
        }

    @property
    def recorded_at(self) -> datetime:
        return self._recorded_at

    @property
    def hor_calibration(self) -> float:
        return self._hor_calibration

    @property
    def hor_calibration_diff(self) -> float:
        return self._hor_calibration_diff

    @property
    def protocol(self) -> Protocol:
        return self._protocol
