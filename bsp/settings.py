from __future__ import annotations

from os.path import expanduser
from pathlib import Path

from PySide6.QtCore import QSettings

from bsp.core import Protocol, log

_DEFAULT_DATA_DIR = Path(expanduser("~/Registros/"))
_DEFAULT_PROTOCOLS_DIR = _DEFAULT_DATA_DIR / "Protocols"


class BSPConfig(QSettings):
    DEVICE_TYPES = [
        # "BiosignalsPlux",
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
    def selected_protocol(self) -> Protocol:
        protocol = self.value("selected_protocol", Protocol.Saccadic)
        if isinstance(protocol, str):
            return Protocol(protocol)

        return protocol

    @selected_protocol.setter
    def selected_protocol(self, protocol: Protocol):
        if isinstance(protocol, str):
            protocol = Protocol(protocol)

        self.setValue("selected_protocol", protocol.value)
        log.debug(f"Set selected protocol: {protocol}")

    @property
    def saccadic_protocol_path(self) -> str:
        return self.value("saccadic_protocol_path", "")

    @saccadic_protocol_path.setter
    def saccadic_protocol_path(self, path: str):
        self.setValue("saccadic_protocol_path", path)
        log.debug(f"Set saccadic protocol path: {path}")

    @property
    def antisaccadic_protocol_path(self) -> str:
        return self.value("antisaccadic_protocol_path", "")

    @antisaccadic_protocol_path.setter
    def antisaccadic_protocol_path(self, path: str):
        self.setValue("antisaccadic_protocol_path", path)
        log.debug(f"Set antisaccadic protocol path: {path}")

    @property
    def pursuit_protocol_path(self) -> str:
        return self.value("pursuit_protocol_path", "")

    @pursuit_protocol_path.setter
    def pursuit_protocol_path(self, path: str):
        self.setValue("pursuit_protocol_path", path)
        log.debug(f"Set pursuit protocol path: {path}")

    @property
    def record_path(self) -> str:
        return self.value("record_path", str(_DEFAULT_DATA_DIR))

    @record_path.setter
    def record_path(self, path: str):
        if not Path(path).exists():
            Path(path).mkdir(parents=True)

        self.setValue("record_path", path)
        log.debug(f"Set record path: {path}")

    @property
    def device_address(self) -> str:
        return self.value("device_address", "/dev/rfcomm0")

    @device_address.setter
    def device_address(self, address: str) -> str:
        return self.setValue("device_address", address)

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
    def stimuli_monitor_width(self) -> int:
        try:
            return int(self.value("stimuli_monitor_width", 0))
        except ValueError:
            return 0

    @stimuli_monitor_width.setter
    def stimuli_monitor_width(self, value: int):
        self.setValue("stimuli_monitor_width", value)

    @property
    def stimuli_monitor_height(self) -> int:
        try:
            return int(self.value("stimuli_monitor_height", 0))
        except ValueError:
            return 0

    @stimuli_monitor_height.setter
    def stimuli_monitor_height(self, value: int):
        self.setValue("stimuli_monitor_height", value)

    @property
    def stimuli_ball_radius(self) -> int:
        try:
            return int(self.value("stimuli_ball_radius", 16))
        except ValueError:
            return 16

    @stimuli_ball_radius.setter
    def stimuli_ball_radius(self, value: int):
        self.setValue("stimuli_ball_radius", value)

    @property
    def resolution(self) -> int:
        if self.device_type == "Bitalino":
            return 10
        return 16


config = BSPConfig()
