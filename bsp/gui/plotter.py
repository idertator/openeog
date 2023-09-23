from numpy import ndarray
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QSplitter, QVBoxLayout, QWidget


class Plotter(QWidget):
    def __init__(
        self,
        parent=None,
        resolution: int = 16,  # in bits
        length: int = 10000,  # in ms
    ):
        super().__init__(parent)

        self.length = length
        self.resolution = resolution

        self._signal_pen = QPen(Qt.blue)
        self._stimulus_pen = QPen(Qt.red)

        self._horizontal = QLineSeries()
        self._horizontal.setUseOpenGL(True)
        self._horizontal.setPen(self._signal_pen)

        self._horizontal_stimulus = QLineSeries()
        self._horizontal_stimulus.setUseOpenGL(True)
        self._horizontal_stimulus.setPen(self._stimulus_pen)

        self._horizontal_x = QValueAxis()
        self._horizontal_x.setRange(0, length)
        self._horizontal_x.setLabelFormat("%g")
        self._horizontal_x.setTitleText("Time (ms)")

        self._horizontal_y = QValueAxis()
        self._horizontal_y.setRange(0, 2**resolution - 1)
        self._horizontal_y.setTitleText("Value")

        self._horizontal_chart = QChart()
        self._horizontal_chart.addSeries(self._horizontal_stimulus)
        self._horizontal_chart.addSeries(self._horizontal)
        self._horizontal_chart.setAxisX(self._horizontal_x, self._horizontal)
        self._horizontal_chart.setAxisX(self._horizontal_x, self._horizontal_stimulus)
        self._horizontal_chart.setAxisY(self._horizontal_y, self._horizontal)
        self._horizontal_chart.setAxisY(self._horizontal_y, self._horizontal_stimulus)
        self._horizontal_chart.legend().hide()
        self._horizontal_chart.setTitle("Horizontal Channel")

        self._horizontal_chart_view = QChartView(self._horizontal_chart)
        self._horizontal_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self._vertical = QLineSeries()
        self._vertical.setUseOpenGL(True)
        self._vertical.setPen(self._signal_pen)

        self._vertical_stimulus = QLineSeries()
        self._vertical_stimulus.setUseOpenGL(True)
        self._vertical_stimulus.setPen(self._stimulus_pen)

        self._vertical_x = QValueAxis()
        self._vertical_x.setRange(0, length)
        self._vertical_x.setLabelFormat("%g")
        self._vertical_x.setTitleText("Time (ms)")

        self._vertical_y = QValueAxis()
        self._vertical_y.setRange(0, 2**resolution - 1)
        self._vertical_y.setTitleText("Value")

        self._vertical_chart = QChart()
        self._vertical_chart.addSeries(self._vertical)
        self._vertical_chart.addSeries(self._vertical_stimulus)
        self._vertical_chart.setAxisX(self._vertical_x, self._vertical)
        self._vertical_chart.setAxisX(self._vertical_x, self._vertical_stimulus)
        self._vertical_chart.setAxisY(self._vertical_y, self._vertical)
        self._vertical_chart.setAxisY(self._vertical_y, self._vertical_stimulus)
        self._vertical_chart.legend().hide()
        self._vertical_chart.setTitle("Vertical Channel")

        self._vertical_chart_view = QChartView(self._vertical_chart)
        self._vertical_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self._splitter = QSplitter()
        self._splitter.addWidget(self._horizontal_chart_view)
        self._splitter.addWidget(self._vertical_chart_view)
        self._splitter.setOrientation(Qt.Orientations.Vertical)

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._splitter)

        self._horizontal_buffer = [QPoint(i, 0) for i in range(length)]
        self._horizontal_stimulus_buffer = [QPoint(i, 0) for i in range(length)]
        self._vertical_buffer = [QPoint(i, 0) for i in range(length)]
        self._vertical_stimulus_buffer = [QPoint(i, 0) for i in range(length)]

        self.setLayout(self._layout)

    def plot_samples(
        self,
        horizontal: ndarray,
        horizontal_stimulus: ndarray,
        vertical: ndarray,
        vertical_stimulus: ndarray,
    ):
        length = len(horizontal)
        start = 0
        if length < self.length:
            start = self.length - length
            for s in range(start):
                self._horizontal_buffer[s].setY(self._horizontal_buffer[s + length].y())
                self._horizontal_stimulus_buffer[s].setY(
                    self._horizontal_stimulus_buffer[s + length].y()
                )
                self._vertical_buffer[s].setY(self._vertical_buffer[s + length].y())
                self._vertical_stimulus_buffer[s].setY(
                    self._vertical_stimulus_buffer[s + length].y()
                )

        idx = 0
        for s in range(start, self.length):
            self._horizontal_buffer[s].setY(horizontal[idx])
            self._horizontal_stimulus_buffer[s].setY(horizontal_stimulus[idx])
            self._vertical_buffer[s].setY(vertical[idx])
            self._vertical_stimulus_buffer[s].setY(vertical_stimulus[idx])
            idx += 1

        self._horizontal.replace(self._horizontal_buffer)
        self._horizontal_stimulus.replace(self._horizontal_stimulus_buffer)
        self._vertical.replace(self._vertical_buffer)
        self._vertical_stimulus.replace(self._vertical_stimulus_buffer)
