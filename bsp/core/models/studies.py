from __future__ import annotations

from datetime import datetime

from bsp.core.calibration import calibration
from bsp.core.models import Protocol

from .enums import TestType
from .hardware import Hardware
from .tests import Test


class Study:
    VERSION = "1.0"

    def __init__(
        self,
        recorded_at: datetime | None,
        tests: list[Test],
        protocol: Protocol,
        hardware: Hardware | None = None,
        hor_calibration: float | None = None,
        hor_calibration_diff: float | None = None,
        ver_calibration: float | None = None,
        ver_calibration_diff: float | None = None,
        errors: int = 0,
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

        self._hardware = hardware
        self._errors = errors

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
            "recorded_at": self._recorded_at.timestamp(),
            "errors": self._errors,
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
    def errors(self) -> int:
        return self._errors

    @errors.setter
    def errors(self, value: int):
        self._errors = value

    @property
    def samples_count(self) -> int:
        total = 0
        for test in self._tests:
            total += test.length
        return total
