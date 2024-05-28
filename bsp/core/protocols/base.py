from __future__ import annotations

from dataclasses import dataclass

from bsp.core.models import Protocol


@dataclass
class ProtocolTemplate:
    protocol: Protocol
    name: str
    length: float

    def save_to_file(self, filename: str):
        raise NotImplementedError()

    @classmethod
    def load_from_file(cls, filename: str) -> ProtocolTemplate:
        raise NotImplementedError()
