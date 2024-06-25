from __future__ import annotations

import logging
from dataclasses import dataclass
from json import dump, load

from bsp.core.models import Protocol

from .base import ProtocolTemplate

log = logging.getLogger("t3")


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
