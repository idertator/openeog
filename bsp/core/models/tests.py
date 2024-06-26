from functools import cached_property

import numpy as np

from bsp.core.denoising import denoise
from bsp.core.saccades import saccades

from .annotations import Annotation, Saccade
from .enums import TestType


class Test(object):
    def __init__(
        self,
        test_type: TestType,
        angle: int,
        hor_stimuli: np.ndarray,
        hor_channel: np.ndarray,
        ver_stimuli: np.ndarray,
        ver_channel: np.ndarray,
        hor_annotations: list[Annotation] = [],
        ver_annotations: list[Annotation] = [],
        fs: int = 1000,
        replica: bool = False,
        **kwargs,
    ):
        self._test_type = test_type
        self._angle = angle
        self._fs = fs
        self._replica = replica

        self._hor_stimuli = hor_stimuli
        self._hor_channel = hor_channel
        self._ver_stimuli = ver_stimuli
        self._ver_channel = ver_channel
        self._hor_annotations = hor_annotations
        self._ver_annotations = ver_annotations

        self._hor_calibration: float = 1.0
        self._ver_calibration: float = 1.0

    def __str__(self):
        if self._replica:
            return "{test} at {angle}° (Replica)".format(
                test=self._test_type.value,
                angle=self._angle,
            )

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
            "replica": self._replica,
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
    def hor_stimuli(self) -> np.ndarray:
        normalized = (self._hor_stimuli - 32768) / 20000
        scaled = normalized.astype(np.single) * (self.angle / 2)
        return scaled

    @property
    def hor_stimuli_raw(self) -> np.ndarray:
        return self._hor_stimuli

    @cached_property
    def hor_channel(self) -> np.ndarray:
        scaled = self._hor_channel.astype(np.single) * self._hor_calibration
        centered = scaled - scaled.mean()
        return denoise(centered)

    @property
    def hor_channel_raw(self) -> np.ndarray:
        return self._hor_channel

    @cached_property
    def ver_stimuli(self) -> np.ndarray:
        normalized = (self._ver_stimuli - 32768) / 20000
        scaled = normalized.astype(np.single) * (self.angle / 2)
        return scaled

    @property
    def ver_stimuli_raw(self) -> np.ndarray:
        return self._ver_stimuli

    @cached_property
    def ver_channel(self) -> np.ndarray:
        scaled = self._ver_channel.astype(np.single) * self._hor_calibration
        centered = scaled - scaled.mean()
        return denoise(centered)

    @property
    def ver_channel_raw(self) -> np.ndarray:
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
