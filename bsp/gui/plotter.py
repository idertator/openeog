from numpy import ndarray
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import QPointF, Qt
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

        self._hor = QLineSeries()
        self._hor.setUseOpenGL(True)
        self._hor.setPen(self._signal_pen)

        self._hor_stimuli = QLineSeries()
        self._hor_stimuli.setUseOpenGL(True)
        self._hor_stimuli.setPen(self._stimulus_pen)

        self._hor_x = QValueAxis()
        self._hor_x.setRange(0, length)
        self._hor_x.setLabelFormat("%g")
        self._hor_x.setTitleText("Tiempo (ms)")

        self._hor_y = QValueAxis()
        self._hor_y.setRange(0, 2**resolution - 1)
        self._hor_y.setTitleText("Valor")

        self._hor_chart = QChart()
        self._hor_chart.addSeries(self._hor_stimuli)
        self._hor_chart.addSeries(self._hor)
        self._hor_chart.setAxisX(self._hor_x, self._hor)
        self._hor_chart.setAxisX(self._hor_x, self._hor_stimuli)
        self._hor_chart.setAxisY(self._hor_y, self._hor)
        self._hor_chart.setAxisY(self._hor_y, self._hor_stimuli)
        self._hor_chart.legend().hide()
        self._hor_chart.setTitle("Canal Horizontal")

        self._hor_chart_view = QChartView(self._hor_chart)
        self._hor_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self._ver = QLineSeries()
        self._ver.setUseOpenGL(True)
        self._ver.setPen(self._signal_pen)

        self._ver_stimulus = QLineSeries()
        self._ver_stimulus.setUseOpenGL(True)
        self._ver_stimulus.setPen(self._stimulus_pen)

        self._ver_x = QValueAxis()
        self._ver_x.setRange(0, length)
        self._ver_x.setLabelFormat("%g")
        self._ver_x.setTitleText("Tiempo (ms)")

        self._ver_y = QValueAxis()
        self._ver_y.setRange(0, 2**resolution - 1)
        self._ver_y.setTitleText("Valor")

        self._ver_chart = QChart()
        self._ver_chart.addSeries(self._ver)
        self._ver_chart.addSeries(self._ver_stimulus)
        self._ver_chart.setAxisX(self._ver_x, self._ver)
        self._ver_chart.setAxisX(self._ver_x, self._ver_stimulus)
        self._ver_chart.setAxisY(self._ver_y, self._ver)
        self._ver_chart.setAxisY(self._ver_y, self._ver_stimulus)
        self._ver_chart.legend().hide()
        self._ver_chart.setTitle("Canal Vertical")

        self._ver_chart_view = QChartView(self._ver_chart)
        self._ver_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self._splitter = QSplitter()
        self._splitter.addWidget(self._hor_chart_view)
        self._splitter.addWidget(self._ver_chart_view)
        self._splitter.setOrientation(Qt.Orientations.Vertical)

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._splitter)

        self._hor_buffer = [QPointF(i, 0) for i in range(length)]
        self._hor_stimuli_buffer = [QPointF(i, 0) for i in range(length)]
        self._ver_buffer = [QPointF(i, 0) for i in range(length)]
        self._ver_stimulus_buffer = [QPointF(i, 0) for i in range(length)]

        self.setLayout(self._layout)

    def plot_samples(
        self,
        hor: ndarray,
        hor_stimuli: ndarray,
        ver: ndarray,
        ver_stimulus: ndarray,
    ):
        length = len(hor)
        start = 0
        if length < self.length:
            start = self.length - length
            for s in range(start):
                self._hor_buffer[s].setY(
                    float(self._hor_buffer[s + length].y()),
                )
                self._hor_stimuli_buffer[s].setY(
                    float(self._hor_stimuli_buffer[s + length].y()),
                )
                self._ver_buffer[s].setY(
                    float(self._ver_buffer[s + length].y()),
                )
                self._ver_stimulus_buffer[s].setY(
                    float(self._ver_stimulus_buffer[s + length].y()),
                )

        idx = 0
        for s in range(start, self.length):
            self._hor_buffer[s].setY(float(hor[idx]))
            self._hor_stimuli_buffer[s].setY(float(hor_stimuli[idx]))
            self._ver_buffer[s].setY(float(ver[idx]))
            self._ver_stimulus_buffer[s].setY(float(ver_stimulus[idx]))
            idx += 1

        self._hor.replace(self._hor_buffer)
        self._hor_stimuli.replace(self._hor_stimuli_buffer)
        self._ver.replace(self._ver_buffer)
        self._ver_stimulus.replace(self._ver_stimulus_buffer)
