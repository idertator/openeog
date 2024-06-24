from os.path import expanduser
from pathlib import Path

from PySide6.QtCore import QSettings

from bsp.core import Protocol, log

DEFAULT_DATA_DIR = Path(expanduser("~/Registros/"))
DEFAULT_PROTOCOLS_DIR = DEFAULT_DATA_DIR / "Protocols"


def protocols_path() -> str:
    settings = QSettings()
    path = settings.value("protocols_path", DEFAULT_PROTOCOLS_DIR)

    if not Path(path).exists():
        Path(path).mkdir(parents=True)

    return str(path)


def set_protocols_path(path: str):
    settings = QSettings()
    settings.setValue("protocols_path", path)
    log.debug(f"Set protocols path: {path}")

    if not Path(path).exists():
        Path(path).mkdir(parents=True)
        log.debug(f"Created protocols path: {path}")


def default_selected_protocol() -> Protocol:
    settings = QSettings()

    protocol = settings.value("default_selected_protocol", Protocol.Saccadic)
    if isinstance(protocol, str):
        return Protocol(protocol)

    return protocol


def set_default_selected_protocol(protocol: Protocol):
    settings = QSettings()

    if isinstance(protocol, str):
        protocol = Protocol(protocol)

    settings.setValue("default_selected_protocol", protocol.value)
    log.debug(f"Set default selected protocol: {protocol}")


def default_saccadic_protocol_path() -> str:
    settings = QSettings()
    return settings.value("default_saccadic_protocol_path", "")


def set_default_saccadic_protocol_path(path: str):
    settings = QSettings()
    settings.setValue("default_saccadic_protocol_path", path)
    log.debug(f"Set default saccadic protocol path: {path}")


def default_antisaccadic_protocol_path() -> str:
    settings = QSettings()
    return settings.value("default_antisaccadic_protocol_path", "")


def set_default_antisaccadic_protocol_path(path: str):
    settings = QSettings()
    settings.setValue("default_antisaccadic_protocol_path", path)
    log.debug(f"Set default antisaccadic protocol path: {path}")


def default_pursuit_protocol_path() -> str:
    settings = QSettings()
    return settings.value("default_pursuit_protocol_path", "")


def set_default_pursuit_protocol_path(path: str):
    settings = QSettings()
    settings.setValue("default_pursuit_protocol_path", path)
    log.debug(f"Set default pursuit protocol path: {path}")
