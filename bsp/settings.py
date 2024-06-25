from __future__ import annotations

from os.path import expanduser
from pathlib import Path

from PySide6.QtCore import QSettings

from bsp.core import Protocol, log

_DEFAULT_DATA_DIR = Path(expanduser("~/Registros/"))
_DEFAULT_PROTOCOLS_DIR = _DEFAULT_DATA_DIR / "Protocols"


class BSPConfig(QSettings):
    DEVICE_TYPES = [
        "BiosignalsPlux",
        "Bitalino",
    ]

    PROTOCOLS = [
        {
            "protocol": Protocol.Saccadic,
            "name": "Protocolo de Sácadas",
            "icon": ":saccades.svg",
        },
        {
            "protocol": Protocol.Antisaccadic,
            "name": "Protocolo Antisacádico",
            "icon": ":antisaccades.svg",
        },
        {
            "protocol": Protocol.Pursuit,
            "name": "Protocolo de Persecución",
            "icon": ":pursuit.svg",
        },
    ]

    @property
    def protocols_path(self) -> str:
        path = self.value("protocols_path", _DEFAULT_PROTOCOLS_DIR)

        if not Path(path).exists():
            Path(path).mkdir(parents=True)

        return str(path)

    @protocols_path.setter
    def protocols_path(self, path: str):
        self.setValue("protocols_path", path)
        log.debug(f"Set protocols path: {path}")

        if not Path(path).exists():
            Path(path).mkdir(parents=True)
            log.debug(f"Created protocols path: {path}")

    @property
    def default_selected_protocol(self) -> Protocol:
        protocol = self.value("default_selected_protocol", Protocol.Saccadic)
        if isinstance(protocol, str):
            return Protocol(protocol)

        return protocol

    @default_selected_protocol.setter
    def default_selected_protocol(self, protocol: Protocol):
        if isinstance(protocol, str):
            protocol = Protocol(protocol)

        self.setValue("default_selected_protocol", protocol.value)
        log.debug(f"Set default selected protocol: {protocol}")

    @property
    def default_saccadic_protocol_path(self) -> str:
        return self.value("default_saccadic_protocol_path", "")

    @default_saccadic_protocol_path.setter
    def default_saccadic_protocol_path(self, path: str):
        self.setValue("default_saccadic_protocol_path", path)
        log.debug(f"Set default saccadic protocol path: {path}")

    @property
    def default_antisaccadic_protocol_path(self) -> str:
        return self.value("default_antisaccadic_protocol_path", "")

    @default_antisaccadic_protocol_path.setter
    def default_antisaccadic_protocol_path(self, path: str):
        self.setValue("default_antisaccadic_protocol_path", path)
        log.debug(f"Set default antisaccadic protocol path: {path}")

    @property
    def default_pursuit_protocol_path(self) -> str:
        return self.value("default_pursuit_protocol_path", "")

    @default_pursuit_protocol_path.setter
    def default_pursuit_protocol_path(self, path: str):
        self.setValue("default_pursuit_protocol_path", path)
        log.debug(f"Set default pursuit protocol path: {path}")

    @property
    def device_address(self) -> str:
        return self.value("device_address", "/dev/rfcomm0")

    @device_address.setter
    def device_address(self, address: str) -> str:
        return self.value("device_address", address)

    @property
    def device_type(self) -> str:
        return self.value("device_type", "BiosignalsPlux")

    @device_type.setter
    def device_type(self, value: str):
        self.setValue("device_type", value)

    @property
    def stimuli_monitor(self) -> str:
        return self.value("stimuli_monitor", "")

    @stimuli_monitor.setter
    def stimuli_monitor(self, value: str):
        self.setValue("stimuli_monitor", value)

    @property
    def resolution(self) -> int:
        if self.device_type == "Bitalino":
            return 10
        return 16


config = BSPConfig()
