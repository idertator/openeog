from __future__ import annotations

from dataclasses import dataclass
from json import dump, load

import numpy as np

from bsp.core.logging import log
from bsp.core.models import Protocol, TestType
from bsp.core.stimuli import pursuit_stimuli, saccadic_stimuli

from .base import ProtocolTemplate


@dataclass
class PursuitProtocolTemplate(ProtocolTemplate):
    pursuit_length: int
    pursuit_speed: float
    include_replicas: bool
    pursuit_10: bool
    pursuit_20: bool
    pursuit_30: bool
    pursuit_60: bool

    @classmethod
    def open(cls, filename: str) -> PursuitProtocolTemplate:
        log.debug(f"Loading protocol: {filename}")

        with open(filename, "rt") as f:
            json = load(f)

        protocol = json.pop("type", None)
        if protocol != Protocol.Pursuit.value:
            raise ValueError(f"Tipo de prueba inválido: {protocol}")

        name = json.get("name", None)
        if not isinstance(name, str) or not name:
            raise ValueError(f"El nombre {name} no es válido")

        calibration_length = json.get("calibration_length", None)
        if not isinstance(calibration_length, (int, float)):
            raise ValueError(f"Longitud de calibración inválida: {calibration_length}")

        if calibration_length < 10 or calibration_length > 100:
            raise ValueError(f"Longitud de calibración inválida: {calibration_length}")

        calibration_count = json.get("calibration_count", None)
        if not isinstance(calibration_count, (int, float)):
            raise ValueError(f"Longitud de calibración inválida: {calibration_count}")

        if calibration_count < 5 or calibration_count > 10:
            raise ValueError(f"Longitud de calibración inválida: {calibration_count}")

        pursuit_length = json.get("pursuit_length", None)
        if not isinstance(pursuit_length, (int, float)):
            raise ValueError("Longitud de persecución inválida")

        if pursuit_length < 10 or pursuit_length > 100:
            raise ValueError("Longitud de persecución inválida")

        pursuit_speed = json.get("pursuit_speed", None)
        if not isinstance(pursuit_speed, (int, float)):
            raise ValueError("Variabilidad sacádica inválida")

        if pursuit_speed < 0.1 or pursuit_speed > 10.0:
            raise ValueError("Variabilidad sacádica inválida")

        return cls(**json)

    def save(self, filename: str):
        with open(filename, "wt") as f:
            dump(self.json, f, indent=4)

    @property
    def json(self) -> dict:
        return (
            {
                "type": Protocol.Pursuit,
            }
            | super().json
            | {
                "pursuit_length": self.pursuit_length,
                "pursuit_speed": self.pursuit_speed,
                "include_replicas": self.include_replicas,
                "pursuit_10": self.pursuit_10,
                "pursuit_20": self.pursuit_20,
                "pursuit_30": self.pursuit_30,
                "pursuit_60": self.pursuit_60,
            }
        )

    @property
    def tests(self) -> list[dict]:
        result = []

        calibration_length = int(self.calibration_length * 1000)

        result.append(
            {
                "test_type": TestType.HorizontalCalibration,
                "angle": 30,
                "hor_stimuli": saccadic_stimuli(
                    length=calibration_length,
                    saccades=self.calibration_count,
                ),
                "hor_channel": np.zeros(calibration_length, dtype=np.uint16),
                "ver_stimuli": np.zeros(calibration_length, dtype=np.uint16),
                "ver_channel": np.zeros(calibration_length, dtype=np.uint16),
            }
        )

        pursuit_length = int(self.pursuit_length * 1000)

        if self.pursuit_10:
            result.append(
                {
                    "test_type": TestType.HorizontalPursuit,
                    "angle": 10,
                    "replica": False,
                    "hor_stimuli": pursuit_stimuli(
                        length=pursuit_length,
                        speed=self.pursuit_speed,
                    ),
                    "hor_channel": np.zeros(pursuit_length, dtype=np.uint16),
                    "ver_stimuli": np.zeros(pursuit_length, dtype=np.uint16),
                    "ver_channel": np.zeros(pursuit_length, dtype=np.uint16),
                }
            )

            if self.include_replicas:
                result.append(
                    {
                        "test_type": TestType.HorizontalPursuit,
                        "angle": 10,
                        "replica": True,
                        "hor_stimuli": pursuit_stimuli(
                            length=pursuit_length,
                            speed=self.pursuit_speed,
                        ),
                        "hor_channel": np.zeros(pursuit_length, dtype=np.uint16),
                        "ver_stimuli": np.zeros(pursuit_length, dtype=np.uint16),
                        "ver_channel": np.zeros(pursuit_length, dtype=np.uint16),
                    }
                )

        if self.pursuit_20:
            result.append(
                {
                    "test_type": TestType.HorizontalPursuit,
                    "angle": 20,
                    "replica": False,
                    "hor_stimuli": pursuit_stimuli(
                        length=pursuit_length,
                        speed=self.pursuit_speed,
                    ),
                    "hor_channel": np.zeros(pursuit_length, dtype=np.uint16),
                    "ver_stimuli": np.zeros(pursuit_length, dtype=np.uint16),
                    "ver_channel": np.zeros(pursuit_length, dtype=np.uint16),
                }
            )

            if self.include_replicas:
                result.append(
                    {
                        "test_type": TestType.HorizontalPursuit,
                        "angle": 20,
                        "replica": True,
                        "hor_stimuli": pursuit_stimuli(
                            length=pursuit_length,
                            speed=self.pursuit_speed,
                        ),
                        "hor_channel": np.zeros(pursuit_length, dtype=np.uint16),
                        "ver_stimuli": np.zeros(pursuit_length, dtype=np.uint16),
                        "ver_channel": np.zeros(pursuit_length, dtype=np.uint16),
                    }
                )

        if self.pursuit_30:
            result.append(
                {
                    "test_type": TestType.HorizontalPursuit,
                    "angle": 30,
                    "replica": False,
                    "hor_stimuli": pursuit_stimuli(
                        length=pursuit_length,
                        speed=self.pursuit_speed,
                    ),
                    "hor_channel": np.zeros(pursuit_length, dtype=np.uint16),
                    "ver_stimuli": np.zeros(pursuit_length, dtype=np.uint16),
                    "ver_channel": np.zeros(pursuit_length, dtype=np.uint16),
                }
            )

            if self.include_replicas:
                result.append(
                    {
                        "test_type": TestType.HorizontalPursuit,
                        "angle": 30,
                        "replica": True,
                        "hor_stimuli": pursuit_stimuli(
                            length=pursuit_length,
                            speed=self.pursuit_speed,
                        ),
                        "hor_channel": np.zeros(pursuit_length, dtype=np.uint16),
                        "ver_stimuli": np.zeros(pursuit_length, dtype=np.uint16),
                        "ver_channel": np.zeros(pursuit_length, dtype=np.uint16),
                    }
                )

        if self.pursuit_60:
            result.append(
                {
                    "test_type": TestType.HorizontalPursuit,
                    "angle": 60,
                    "replica": False,
                    "hor_stimuli": pursuit_stimuli(
                        length=pursuit_length,
                        speed=self.pursuit_speed,
                    ),
                    "hor_channel": np.zeros(pursuit_length, dtype=np.uint16),
                    "ver_stimuli": np.zeros(pursuit_length, dtype=np.uint16),
                    "ver_channel": np.zeros(pursuit_length, dtype=np.uint16),
                }
            )

            if self.include_replicas:
                result.append(
                    {
                        "test_type": TestType.HorizontalPursuit,
                        "angle": 60,
                        "replica": True,
                        "hor_stimuli": pursuit_stimuli(
                            length=pursuit_length,
                            speed=self.pursuit_speed,
                        ),
                        "hor_channel": np.zeros(pursuit_length, dtype=np.uint16),
                        "ver_stimuli": np.zeros(pursuit_length, dtype=np.uint16),
                        "ver_channel": np.zeros(pursuit_length, dtype=np.uint16),
                    }
                )

        result.append(
            {
                "test_type": TestType.HorizontalCalibration,
                "angle": 30,
                "hor_stimuli": saccadic_stimuli(
                    length=calibration_length,
                    saccades=self.calibration_count,
                ),
                "hor_channel": np.zeros(calibration_length, dtype=np.uint16),
                "ver_stimuli": np.zeros(calibration_length, dtype=np.uint16),
                "ver_channel": np.zeros(calibration_length, dtype=np.uint16),
            }
        )

        return result
