from PySide6.QtCore import QObject, QRect, QSize, Slot
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QApplication


class ScreensManager(QObject):
    def __init__(self, app: QApplication):
        super().__init__()

        self.app = app
        self._screens = {
            screen.name(): {
                "screen_size": screen.size(),
                "physical_size": screen.physicalSize(),
                "geometry": screen.geometry(),
                "rate": int(screen.refreshRate()),
                "dpi": float(screen.physicalDotsPerInch()),
            }
            for screen in self.app.screens()
        }

        self.app.screenAdded.connect(self.on_screen_added)
        self.app.screenRemoved.connect(self.on_screen_removed)

    @property
    def screen_list(self) -> list[str]:
        return list(self._screens.keys())

    def screen_size(self, screen: str) -> QSize | None:
        if screen in self._screens:
            return self._screens[screen]["screen_size"]
        return None

    def physical_size(self, screen: str) -> QSize | None:
        if screen in self._screens:
            return self._screens[screen]["physical_size"]
        return None

    def geometry(self, screen: str) -> QRect | None:
        if screen in self._screens:
            return self._screens[screen]["geometry"]
        return None

    def refresh_rate(self, screen: str) -> int | None:
        if screen in self._screens:
            return self._screens[screen]["rate"]
        return None

    def dpi(self, screen: str) -> float:
        if screen in self._screens:
            return self._screens[screen]["dpi"]
        return 1.0

    @Slot()
    def on_screen_added(self, screen: QScreen):
        self._screens[screen.name()] = {
            "screen_size": screen.size(),
            "physical_size": screen.physicalSize(),
            "geometry": screen.geometry(),
        }

    @Slot()
    def on_screen_removed(self, screen: QScreen):
        del self._screens[screen.name()]
