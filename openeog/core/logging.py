import logging
from os.path import dirname

from termcolor import colored

BASE_DIR = dirname(dirname(__file__))


class OpenEOGDebugFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        match record.levelname:
            case "DEBUG":
                color = "cyan"
                icon = "⚙"
            case "INFO":
                color = "blue"
                icon = "ⓘ"
            case "WARNING":
                color = "yellow"
                icon = "⚠"
            case "ERROR":
                color = "red"
                icon = "✖"
            case "CRITICAL":
                color = "red"
                icon = "☠"
            case _:
                color = "white"
                icon = "➤"

        path = record.pathname
        if path.startswith(BASE_DIR):
            path = path[len(BASE_DIR) + 1 :]

        return colored(
            "{icon}  {path}:{line} {msg}".format(
                icon=icon,
                path=path,
                line=record.lineno,
                msg=record.getMessage(),
            ),
            color,
        )


formatter = OpenEOGDebugFormatter()

handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

log = logging.getLogger("openeog")
log.setLevel(logging.DEBUG)
log.addHandler(handler)
