from math import radians, tan

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QKeyEvent, QPainter, QPaintEvent, QResizeEvent
from PySide6.QtWidgets import QWidget

from .screens import ScreensManager
from .settings import SettingsDialog


class Stimulator(QWidget):
    MAX_DISTANCE_PERCENTAGE = 0.9
    MAX_ANGLE = 60

    initialized = Signal()
    started = Signal()
    cancel = Signal()

    def __init__(
        self,
        screens: ScreensManager,
        settings: SettingsDialog,
        ball_ratio: float = 60,  # in mm
    ):
        super().__init__()
        self._screens = screens
        self._settings = settings

        self._stimuli_screen = self._settings.stimuli_monitor
        physical_size = self._screens.physical_size(self._stimuli_screen)

        self._width = physical_size.width()
        self._height = physical_size.height()

        self._x_scale = float(self.width()) / float(self._width)
        self._y_scale = float(self.height()) / float(self._height)

        self._dpi_scale = screens.dpi(self._stimuli_screen) / 136

        self._ball_ratio = ball_ratio * self._x_scale * self._dpi_scale

        self._msg = ""
        self._ball_position: tuple[int, int] | None = None
        self._subject_distance: int = 0  # in mm
        self._initialized = False

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        background_color = QColor(0, 0, 0)
        foreground_color = QColor(255, 255, 255)

        painter.setBackground(background_color)
        painter.fillRect(self.rect(), background_color)

        painter.setPen(foreground_color)
        painter.setBrush(foreground_color)

        if self._msg:
            painter.save()

            font = painter.font()
            font.setPixelSize(48)

            painter.setFont(font)
            painter.drawText(
                self.rect(),
                Qt.AlignHCenter | Qt.AlignVCenter,
                self._msg,
            )

            painter.restore()
        else:
            painter.drawEllipse(
                self._ball_position[0],
                self._ball_position[1],
                self._ball_ratio,
                self._ball_ratio,
            )

        painter.end()

    def resizeEvent(self, event: QResizeEvent):
        self._x_scale = float(event.size().width()) / float(self._width)
        self._y_scale = float(event.size().height()) / float(self._height)
        self.update()

    def keyPressEvent(self, event: QKeyEvent):
        if (event.modifiers() & Qt.ControlModifier) and event.key() == Qt.Key_C:
            self.cancel.emit()

        elif event.key() == Qt.Key_Space:
            if not self._initialized:
                self._initialized = True
                self.initialized.emit()
            else:
                self.started.emit()

    def open(self):
        self._subject_distance = self.subject_distance
        self._initialized = False
        self.set_message(
            "Siente al sujeto a una distancia de {distance}m de la pantalla".format(
                distance=round(self._subject_distance / 1000.0, 2)
            )
        )

        geometry = self._screens.geometry(self._stimuli_screen)
        self.move(geometry.left(), geometry.top())
        self.showFullScreen()
        self.repaint()

    def set_ball_angle(
        self,
        hor_angle: float,
        ver_angle: float,
    ):
        self._msg = ""

        delta_h = (tan(radians(hor_angle / 2)) * self._subject_distance) * 2
        delta_v = (tan(radians(ver_angle / 2)) * self._subject_distance) * 2

        center = self.rect().center()

        self._ball_position = (
            int(center.x() + (delta_h * self._x_scale)),
            int(center.y() + (delta_v * self._y_scale)),
        )

        self.update()

    def set_message(self, msg: str):
        self._msg = msg
        self._ball_position = None
        self.update()

    @property
    def subject_distance(self) -> int:
        """Distance from the subject to the screen in milimeters"""
        hor_distance = self._width * self.MAX_DISTANCE_PERCENTAGE
        return (hor_distance / 2.0) / tan(radians(self.MAX_ANGLE / 2.0))
