from datetime import datetime
from enum import StrEnum

from numpy import ndarray


class TestType(StrEnum):
    HorizontalCalibration = "Horizontal Calibration"
    HorizontalSaccadicTest = "Horizontal Saccadic Test"


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

    @property
    def horizontal_stimuli(self) -> ndarray:
        return self._horizontal_stimuli

    @property
    def horizontal_channel(self) -> ndarray:
        return self._horizontal_channel

    @property
    def vertical_stimuli(self) -> ndarray:
        return self._vertical_stimuli

    @property
    def vertical_channel(self) -> ndarray:
        return self._vertical_channel


class Study:
    VERSION = "1.0"

    def __init__(
        self,
        recorded_at: datetime | None = None,
        *tests: list[Test],
        **kwargs,
    ):
        self._recorded_at = recorded_at or datetime.now()
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
        }

    @property
    def recorded_at(self) -> datetime:
        return self._recorded_at
