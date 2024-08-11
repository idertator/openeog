import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PySide6 import QtGui as qg
from PySide6 import QtWidgets as qw

from openeog.core import models


class VisualizerToolbar(NavigationToolbar):
    def __init__(self, canvas, parent, coordinates=True):
        super().__init__(canvas, parent, coordinates)

        # Add a toggle button for the horizontal channel
        self.toggle_horizontal_action = qg.QAction(
            qg.QIcon(":horizontal.svg"),
            "Toggle Horizontal",
            self,
        )
        self.toggle_horizontal_action.setCheckable(True)
        self.toggle_horizontal_action.setChecked(True)
        self.toggle_horizontal_action.triggered.connect(self.parent().toggle_horizontal)
        self.addAction(self.toggle_horizontal_action)

        # Add a toggle button for the vertical channel
        self.toggle_vertical_action = qg.QAction(
            qg.QIcon(":vertical.svg"),
            "Toggle Vertical",
            self,
        )
        self.toggle_vertical_action.setCheckable(True)
        self.toggle_vertical_action.setChecked(True)
        self.toggle_vertical_action.triggered.connect(self.parent().toggle_vertical)
        self.addAction(self.toggle_vertical_action)

    def toggle_horizontal(self):
        # Pass the toggle request to the main widget
        self.parent().toggle_horizontal()

    def toggle_vertical(self):
        # Pass the toggle request to the main widget
        self.parent().toggle_vertical()


class Visualizer(qw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.test = None
        self.horizontal_visible = True
        self.vertical_visible = False
        self._setup_gui()

    def _setup_gui(self):
        layout = qw.QVBoxLayout(self)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.toolbar = VisualizerToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)

        self.setLayout(layout)

    def plot(self, test: models.Test | None = None):
        if test is None:
            return
        self.test = test
        self.redraw_plots()

    def redraw_plots(self):
        self.figure.clear()
        if self.test is None:
            self.canvas.draw()
            return

        time = np.arange(0, len(self.test.hor_channel)) / self.test.fs

        if self.horizontal_visible:
            self.ax1 = self.figure.add_subplot(
                211 if self.vertical_visible else 111,
                title="Canal Horizontal",
            )
            self.ax1.plot(
                time,
                self.test.hor_channel,
                label="Horizontal",
            )
            self.ax1.plot(
                time,
                self.test.hor_stimuli,
                label="Horizontal",
            )
            self.ax1.set_ylabel("Amplitude")
            self.ax1.grid(True)

        if self.vertical_visible:
            ax_number = 212 if self.horizontal_visible else 111
            self.ax2 = self.figure.add_subplot(
                ax_number,
                title="Canal Vertical",
            )
            self.ax2.plot(
                time,
                self.test.ver_channel,
                label="Vertical",
            )
            self.ax2.plot(
                time,
                self.test.ver_stimuli,
                label="Vertical",
            )
            self.ax2.set_ylabel("Amplitude")
            self.ax2.set_xlabel("Time (s)")
            self.ax2.grid(True)

        self.figure.tight_layout()
        self.canvas.draw()

    def toggle_horizontal(self):
        self.horizontal_visible = not self.horizontal_visible
        self.toolbar.toggle_horizontal_action.setChecked(self.horizontal_visible)
        self.redraw_plots()

    def toggle_vertical(self):
        self.vertical_visible = not self.vertical_visible
        self.toolbar.toggle_vertical_action.setChecked(self.vertical_visible)
        self.redraw_plots()
