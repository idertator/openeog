from __future__ import annotations

from dataclasses import dataclass
from json import dump, load

from bsp.core.logging import log
from bsp.core.models import Protocol

from .base import ProtocolTemplate


@dataclass
class SaccadicProtocolTemplate(ProtocolTemplate):
    saccadic_length: int
    saccadic_variability: float
    saccadic_count: int
    include_replicas: bool
    saccadic_10: bool
    saccadic_20: bool
    saccadic_30: bool
    saccadic_60: bool

    @classmethod
    def open(cls, filename: str) -> SaccadicProtocolTemplate:
        log.debug(f"Loading protocol: {filename}")

        with open(filename, "rt") as f:
            json = load(f)

        protocol = json.pop("type", None)
        if protocol != Protocol.Saccadic.value:
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

        saccadic_length = json.get("saccadic_length", None)
        if not isinstance(saccadic_length, (int, float)):
            raise ValueError("Longitud sacádica inválida")

        if saccadic_length < 10 or saccadic_length > 100:
            raise ValueError("Longitud sacádica inválida")

        saccadic_variability = json.get("saccadic_variability", None)
        if not isinstance(saccadic_variability, (int, float)):
            raise ValueError("Variabilidad sacádica inválida")

        if saccadic_variability < 0.1 or saccadic_variability > 100:
            raise ValueError("Variabilidad sacádica inválida")

        saccadic_count = json.get("saccadic_count", None)
        if not isinstance(saccadic_count, (int, float)):
            raise ValueError(f"Cantidad de sácadas inválida: {saccadic_count}")

        if saccadic_count < 5 or saccadic_count > 30:
            raise ValueError(f"Cantidad de sácadas inválida: {saccadic_count}")

        return cls(**json)

    def save(self, filename: str):
        with open(filename, "wt") as f:
            dump(self.json, f, indent=4)

    @property
    def json(self) -> dict:
        return (
            {
                "type": Protocol.Saccadic,
            }
            | super().json
            | {
                "saccadic_length": self.saccadic_length,
                "saccadic_variability": self.saccadic_variability,
                "saccadic_count": self.saccadic_count,
                "include_replicas": self.include_replicas,
                "saccadic_10": self.saccadic_10,
                "saccadic_20": self.saccadic_20,
                "saccadic_30": self.saccadic_30,
                "saccadic_60": self.saccadic_60,
            }
        )
