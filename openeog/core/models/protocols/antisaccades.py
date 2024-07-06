from __future__ import annotations

from dataclasses import dataclass
from json import dump, load

import numpy as np

from openeog.core.logging import log
from openeog.core.models import Protocol, TestType
from openeog.core.stimuli import saccadic_stimuli

from .base import ProtocolTemplate


@dataclass
class AntisaccadicProtocolTemplate(ProtocolTemplate):
    antisaccadic_length: int
    antisaccadic_variability: float
    antisaccadic_count: int
    include_replicas: bool = False
    antisaccadic_10: bool = False
    antisaccadic_20: bool = False
    antisaccadic_30: bool = False
    antisaccadic_40: bool = False
    antisaccadic_50: bool = False
    antisaccadic_60: bool = False

    @classmethod
    def open(cls, filename: str) -> AntisaccadicProtocolTemplate:
        log.debug(f"Loading protocol: {filename}")

        with open(filename, "rt") as f:
            json = load(f)

        protocol = json.pop("type", None)
        if protocol != Protocol.Antisaccadic.value:
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

        antisaccadic_length = json.get("antisaccadic_length", None)
        if not isinstance(antisaccadic_length, (int, float)):
            raise ValueError("Longitud antisacádica inválida")

        if antisaccadic_length < 10 or antisaccadic_length > 100:
            raise ValueError("Longitud antisacádica inválida")

        antisaccadic_variability = json.get("antisaccadic_variability", None)
        if not isinstance(antisaccadic_variability, (int, float)):
            raise ValueError("Variabilidad antisacádica inválida")

        if antisaccadic_variability < 0.1 or antisaccadic_variability > 100:
            raise ValueError("Variabilidad antisacádica inválida")

        antisaccadic_count = json.get("antisaccadic_count", None)
        if not isinstance(antisaccadic_count, (int, float)):
            raise ValueError(f"Cantidad de antisácadas inválida: {antisaccadic_count}")

        if antisaccadic_count < 5 or antisaccadic_count > 30:
            raise ValueError(f"Cantidad de antisácadas inválida: {antisaccadic_count}")

        return cls(**json)

    def save(self, filename: str):
        with open(filename, "wt") as f:
            dump(self.json, f, indent=4)

    @property
    def json(self) -> dict:
        return (
            {
                "type": Protocol.Antisaccadic,
            }
            | super().json
            | {
                "antisaccadic_length": self.antisaccadic_length,
                "antisaccadic_variability": self.antisaccadic_variability,
                "antisaccadic_count": self.antisaccadic_count,
                "include_replicas": self.include_replicas,
                "antisaccadic_10": self.antisaccadic_10,
                "antisaccadic_20": self.antisaccadic_20,
                "antisaccadic_30": self.antisaccadic_30,
                "antisaccadic_40": self.antisaccadic_40,
                "antisaccadic_50": self.antisaccadic_50,
                "antisaccadic_60": self.antisaccadic_60,
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
                "replica": False,
                "hor_stimuli": saccadic_stimuli(
                    length=calibration_length,
                    saccades=self.calibration_count,
                ),
                "hor_channel": np.zeros(calibration_length, dtype=np.uint16),
                "ver_stimuli": np.zeros(calibration_length, dtype=np.uint16),
                "ver_channel": np.zeros(calibration_length, dtype=np.uint16),
            }
        )

        saccades_samples = int(self.antisaccadic_length * 1000)

        if self.antisaccadic_10:
            result.append(
                {
                    "test_type": TestType.HorizontalAntisaccadic,
                    "angle": 10,
                    "replica": False,
                    "hor_stimuli": saccadic_stimuli(
                        length=saccades_samples,
                        saccades=self.antisaccadic_count,
                    ),
                    "hor_channel": np.zeros(saccades_samples, dtype=np.uint16),
                    "ver_stimuli": np.zeros(saccades_samples, dtype=np.uint16),
                    "ver_channel": np.zeros(saccades_samples, dtype=np.uint16),
                }
            )

            if self.include_replicas:
                result.append(
                    {
                        "test_type": TestType.HorizontalAntisaccadic,
                        "angle": 10,
                        "replica": True,
                        "hor_stimuli": saccadic_stimuli(
                            length=saccades_samples,
                            saccades=self.antisaccadic_count,
                        ),
                        "hor_channel": np.zeros(saccades_samples, dtype=np.uint16),
                        "ver_stimuli": np.zeros(saccades_samples, dtype=np.uint16),
                        "ver_channel": np.zeros(saccades_samples, dtype=np.uint16),
                    }
                )

        if self.antisaccadic_20:
            result.append(
                {
                    "test_type": TestType.HorizontalAntisaccadic,
                    "angle": 20,
                    "replica": False,
                    "hor_stimuli": saccadic_stimuli(
                        length=saccades_samples,
                        saccades=self.antisaccadic_count,
                    ),
                    "hor_channel": np.zeros(saccades_samples, dtype=np.uint16),
                    "ver_stimuli": np.zeros(saccades_samples, dtype=np.uint16),
                    "ver_channel": np.zeros(saccades_samples, dtype=np.uint16),
                }
            )

            if self.include_replicas:
                result.append(
                    {
                        "test_type": TestType.HorizontalAntisaccadic,
                        "angle": 20,
                        "replica": True,
                        "hor_stimuli": saccadic_stimuli(
                            length=saccades_samples,
                            saccades=self.antisaccadic_count,
                        ),
                        "hor_channel": np.zeros(saccades_samples, dtype=np.uint16),
                        "ver_stimuli": np.zeros(saccades_samples, dtype=np.uint16),
                        "ver_channel": np.zeros(saccades_samples, dtype=np.uint16),
                    }
                )

        if self.antisaccadic_30:
            result.append(
                {
                    "test_type": TestType.HorizontalAntisaccadic,
                    "angle": 30,
                    "replica": False,
                    "hor_stimuli": saccadic_stimuli(
                        length=saccades_samples,
                        saccades=self.antisaccadic_count,
                    ),
                    "hor_channel": np.zeros(saccades_samples, dtype=np.uint16),
                    "ver_stimuli": np.zeros(saccades_samples, dtype=np.uint16),
                    "ver_channel": np.zeros(saccades_samples, dtype=np.uint16),
                }
            )

            if self.include_replicas:
                result.append(
                    {
                        "test_type": TestType.HorizontalAntisaccadic,
                        "angle": 30,
                        "replica": True,
                        "hor_stimuli": saccadic_stimuli(
                            length=saccades_samples,
                            saccades=self.antisaccadic_count,
                        ),
                        "hor_channel": np.zeros(saccades_samples, dtype=np.uint16),
                        "ver_stimuli": np.zeros(saccades_samples, dtype=np.uint16),
                        "ver_channel": np.zeros(saccades_samples, dtype=np.uint16),
                    }
                )

        if self.antisaccadic_40:
            result.append(
                {
                    "test_type": TestType.HorizontalAntisaccadic,
                    "angle": 40,
                    "replica": False,
                    "hor_stimuli": saccadic_stimuli(
                        length=saccades_samples,
                        saccades=self.antisaccadic_count,
                    ),
                    "hor_channel": np.zeros(saccades_samples, dtype=np.uint16),
                    "ver_stimuli": np.zeros(saccades_samples, dtype=np.uint16),
                    "ver_channel": np.zeros(saccades_samples, dtype=np.uint16),
                }
            )

            if self.include_replicas:
                result.append(
                    {
                        "test_type": TestType.HorizontalAntisaccadic,
                        "angle": 40,
                        "replica": True,
                        "hor_stimuli": saccadic_stimuli(
                            length=saccades_samples,
                            saccades=self.antisaccadic_count,
                        ),
                        "hor_channel": np.zeros(saccades_samples, dtype=np.uint16),
                        "ver_stimuli": np.zeros(saccades_samples, dtype=np.uint16),
                        "ver_channel": np.zeros(saccades_samples, dtype=np.uint16),
                    }
                )

        if self.antisaccadic_50:
            result.append(
                {
                    "test_type": TestType.HorizontalAntisaccadic,
                    "angle": 50,
                    "replica": False,
                    "hor_stimuli": saccadic_stimuli(
                        length=saccades_samples,
                        saccades=self.antisaccadic_count,
                    ),
                    "hor_channel": np.zeros(saccades_samples, dtype=np.uint16),
                    "ver_stimuli": np.zeros(saccades_samples, dtype=np.uint16),
                    "ver_channel": np.zeros(saccades_samples, dtype=np.uint16),
                }
            )

            if self.include_replicas:
                result.append(
                    {
                        "test_type": TestType.HorizontalAntisaccadic,
                        "angle": 50,
                        "replica": True,
                        "hor_stimuli": saccadic_stimuli(
                            length=saccades_samples,
                            saccades=self.antisaccadic_count,
                        ),
                        "hor_channel": np.zeros(saccades_samples, dtype=np.uint16),
                        "ver_stimuli": np.zeros(saccades_samples, dtype=np.uint16),
                        "ver_channel": np.zeros(saccades_samples, dtype=np.uint16),
                    }
                )

        if self.antisaccadic_60:
            result.append(
                {
                    "test_type": TestType.HorizontalAntisaccadic,
                    "angle": 60,
                    "replica": False,
                    "hor_stimuli": saccadic_stimuli(
                        length=saccades_samples,
                        saccades=self.antisaccadic_count,
                    ),
                    "hor_channel": np.zeros(saccades_samples, dtype=np.uint16),
                    "ver_stimuli": np.zeros(saccades_samples, dtype=np.uint16),
                    "ver_channel": np.zeros(saccades_samples, dtype=np.uint16),
                }
            )

            if self.include_replicas:
                result.append(
                    {
                        "test_type": TestType.HorizontalAntisaccadic,
                        "angle": 60,
                        "replica": True,
                        "hor_stimuli": saccadic_stimuli(
                            length=saccades_samples,
                            saccades=self.antisaccadic_count,
                        ),
                        "hor_channel": np.zeros(saccades_samples, dtype=np.uint16),
                        "ver_stimuli": np.zeros(saccades_samples, dtype=np.uint16),
                        "ver_channel": np.zeros(saccades_samples, dtype=np.uint16),
                    }
                )

        result.append(
            {
                "test_type": TestType.HorizontalCalibration,
                "angle": 30,
                "replica": True,
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
