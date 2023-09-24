from datetime import datetime
from enum import StrEnum
from functools import cached_property

from numpy import ndarray, single

from .calibration import calibration
from .denoising import denoise


class TestType(StrEnum):
    HorizontalCalibration = "Horizontal Calibration"
    HorizontalSaccadicTest = "Horizontal Saccadic Test"
    VerticalCalibration = "Vertical Calibration"


class Test:
    def __init__(
        self,
        test_type: TestType,
        angle: int,
        horizontal_stimuli: ndarray,
        horizontal_channel: ndarray,
        vertical_stimuli: ndarray,
        vertical_channel: ndarray,
        fs: int = 1000,
        **kwargs,
    ):
        self._test_type = test_type
        self._angle = angle
        self._fs = fs

        self._horizontal_stimuli = horizontal_stimuli
        self._horizontal_channel = horizontal_channel
        self._vertical_stimuli = vertical_stimuli
        self._vertical_channel = vertical_channel

        self._horizontal_calibration: float = 1.0
        self._vertical_calibration: float = 1.0

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
            "length": len(self._horizontal_stimuli),
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
    def horizontal_stimuli(self) -> ndarray:
        normalized = (self._horizontal_stimuli - 32768) / 20000
        scaled = normalized.astype(single) * (self.angle / 2)
        return scaled

    @cached_property
    def horizontal_channel(self) -> ndarray:
        scaled = self._horizontal_channel.astype(single) * self._horizontal_calibration
        centered = scaled - scaled.mean()
        return denoise(centered)

    @cached_property
    def vertical_stimuli(self) -> ndarray:
        normalized = (self._vertical_stimuli - 32768) / 20000
        scaled = normalized.astype(single) * (self.angle / 2)
        return scaled

    @cached_property
    def vertical_channel(self) -> ndarray:
        scaled = self._vertical_channel.astype(single) * self._horizontal_calibration
        centered = scaled - scaled.mean()
        return denoise(centered)

    @property
    def horizontal_calibration(self) -> float:
        return self._horizontal_calibration

    @horizontal_calibration.setter
    def horizontal_calibration(self, value: float):
        self._horizontal_calibration = value or 1.0

    @property
    def vertical_calibration(self) -> float:
        return self._vertical_calibration

    @vertical_calibration.setter
    def vertical_calibration(self, value: float):
        self._vertical_calibration = value or 1.0


class Study:
    VERSION = "1.0"

    def __init__(
        self,
        recorded_at: datetime | None,
        tests: list[Test],
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
                initial=initial_calibration.horizontal_channel,
                final=final_calibration.horizontal_channel,
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
                    initial=initial_calibration.vertical_channel,
                    final=final_calibration.vertical_channel,
                    angle=initial_calibration.angle,
                )

        self._ver_calibration = ver_calibration or 1.0
        self._ver_calibration_diff = ver_calibration_diff

        for test in tests:
            test.horizontal_calibration = self._hor_calibration or 1.0

        self._tests = tests

    def __str__(self):
        return "Study recorded at {recorded_at} with {num_tests} tests".format(
            recorded_at=self._recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
            num_tests=len(self._tests),
        )

    def __len__(self):
        return len(self._tests)

    def __getitem__(self, index: int):
        return self._tests[index]

    @property
    def json(self) -> dict:
        return {
            "version": self.VERSION,
            "recorded_at": self._recorded_at.timestamp(),
            "tests": [test.json for test in self._tests],
            "hor_calibration": self.hor_calibration,
            "hor_calibration_diff": self.hor_calibration_diff,
            "ver_calibration": self.ver_calibration,
            "ver_calibration_diff": self.ver_calibration_diff,
        }

    @property
    def recorded_at(self) -> datetime:
        return self._recorded_at
