from dataclasses import dataclass

from bsp.core.models import Protocol

from .base import ProtocolTemplate


@dataclass
class SaccadicProtocolTemplate(ProtocolTemplate):
    saccades: int
    variability: float
    protocol: Protocol = Protocol.Saccadic

    def save_to_file(self, filename: str):
        raise NotImplementedError()

    @classmethod
    def load_from_file(cls, filename: str) -> ProtocolTemplate:
        raise NotImplementedError()
