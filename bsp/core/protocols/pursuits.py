from dataclasses import dataclass

from bsp.core.models import Protocol

from .base import ProtocolTemplate


@dataclass
class PursuitProtocolTemplate(ProtocolTemplate):
    velocity: float
    protocol: Protocol = Protocol.Pursuit

    def save_to_file(self, filename: str):
        raise NotImplementedError()

    @classmethod
    def load_from_file(cls, filename: str) -> ProtocolTemplate:
        raise NotImplementedError()
