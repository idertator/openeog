from __future__ import annotations

from datetime import datetime

from openeog.core.models import Protocol

from .conditions import Conditions
from .hardware import Hardware
from .tests import Test


class Study:
    VERSION = "1.0"

    def __init__(
        self,
        recorded_at: datetime | None,
        protocol: Protocol,
        tests: list[Test],
        hardware: Hardware | None = None,
        conditions: Conditions | None = None,
        hor_calibration: float | None = None,
        hor_calibration_diff: float | None = None,
        ver_calibration: float | None = None,
        ver_calibration_diff: float | None = None,
        **kwargs,
    ):
        self._recorded_at = recorded_at or datetime.now()

        self._hor_calibration = hor_calibration or 1.0
        self._hor_calibration_diff = hor_calibration_diff

        self._ver_calibration = ver_calibration or 1.0
        self._ver_calibration_diff = ver_calibration_diff

        for test in tests:
            test.hor_calibration = self._hor_calibration or 1.0

        self._tests = tests
        self._protocol = protocol

        self._hardware = hardware
        self._conditions = conditions

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
        if isinstance(self._protocol, Protocol):
            protocol = self._protocol.value
        else:
            protocol = self._protocol

        return {
            "version": self.VERSION,
            "hardware": self._hardware.json if self._hardware else None,
            "conditions": self._conditions.json if self._conditions else None,
            "recorded_at": self._recorded_at.timestamp(),
            "protocol": protocol,
            "tests": [test.json for test in self._tests],
            "hor_calibration": float(self._hor_calibration or 1.0),
            "hor_calibration_diff": float(self._hor_calibration_diff or 1.0),
            "ver_calibration": float(self._ver_calibration or 1.0),
            "ver_calibration_diff": float(self._ver_calibration_diff or 1.0),
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

    @property
    def hardware(self) -> Hardware | None:
        return self._hardware

    @hardware.setter
    def hardware(self, value: Hardware | None):
        self._hardware = value

    @property
    def conditions(self) -> Conditions:
        return self._conditions

    @conditions.setter
    def conditions(self, value: Conditions | None):
        self._conditions = value

    @property
    def samples_count(self) -> int:
        total = 0
        for test in self._tests:
            total += test.length
        return total

    @property
    def error_rate(self) -> float:
        if self.samples_count and self.conditions:
            return (self.conditions.errors / self.samples_count) * 100.0
        return 0.0
