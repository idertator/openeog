from dataclasses import dataclass

from .enums import Device, Protocol
from .protocols import ProtocolTemplate


@dataclass
class Session:
    name: str
    path: str
    protocol: Protocol
    template: ProtocolTemplate
    device: Device
    address: str
    stimuli_monitor: str
