from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProtocolTemplate:
    name: str
    calibration_length: float
    calibration_count: int

    @property
    def json(self) -> dict:
        return {
            "name": self.name,
            "calibration_length": self.calibration_length,
            "calibration_count": self.calibration_count,
        }
