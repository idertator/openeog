from os.path import basename, dirname

from PySide6 import QtGui as qg
from PySide6 import QtWidgets as qw

from openeog.core import models
from openeog.core.io import load_study
from openeog.core.logging import log
from openeog.settings import config

from . import resources  # noqa
from .visualizer import Visualizer


class MainWindow(qw.QMainWindow):
    def __init__(self):
        super().__init__()

        self._study: models.Study | None = None
        self._test: models.Test | None = None

        self._setup_gui()

    def _setup_gui(self):
        self.setWindowTitle("OpenEOG Editor")

        # Create the left toolbar with actions
        self._left_toolbar = self.addToolBar("Main")
        self._left_toolbar.setMovable(False)

        self._open_action = qg.QAction(
            qg.QIcon(":open.svg"),
            "&Abrir Estudio",
            self,
        )
        self._open_action.triggered.connect(self._on_open_clicked)
        self._left_toolbar.addAction(self._open_action)

        # Create the right toolbar with combo box
        self._right_toolbar = self.addToolBar("Test")
        self._right_toolbar.setMovable(False)
        self._right_toolbar.setSizePolicy(
            qw.QSizePolicy.Minimum,
            qw.QSizePolicy.Fixed,
        )

        self._tests_combo = qw.QComboBox()
        self._tests_combo.setFixedWidth(300)
        self._tests_combo.setSizePolicy(
            qw.QSizePolicy.Fixed,
            qw.QSizePolicy.Expanding,
        )

        self._tests_layout = qw.QHBoxLayout()
        self._tests_layout.setContentsMargins(0, 0, 0, 0)
        self._tests_layout.addStretch()
        self._tests_layout.addWidget(self._tests_combo)

        self._tests_container = qw.QWidget()
        self._tests_container.setLayout(self._tests_layout)

        self._right_toolbar.addWidget(self._tests_container)
        self._right_toolbar.setVisible(False)

        self._visualizer = Visualizer()
        self._visualizer.setVisible(False)
        self.setCentralWidget(self._visualizer)

    @property
    def study(self) -> models.Study | None:
        return self._study

    @study.setter
    def study(self, value: models.Study | None):
        self._tests_combo.clear()
        if value is not None:
            self._tests_combo.addItems(
                [f"{idx + 1:02} - {test}" for idx, test in enumerate(value)]
            )
            self._right_toolbar.setVisible(True)
            self.test = value[0]
            self._tests_combo.currentIndexChanged.connect(
                self._on_test_changed_index,
            )
        else:
            self._tests_combo.currentIndexChanged.disconnect(
                self._on_test_changed_index,
            )
            self._right_toolbar.setVisible(False)
            self.test = None

        self._study = value
        log.info("Set study: %s", self.study)

    @property
    def test(self) -> models.Test | None:
        return self._test

    @test.setter
    def test(self, value: models.Test | None):
        if value:
            self._visualizer.plot(value)
            self._visualizer.setVisible(True)
        else:
            self._visualizer.plot(None)
            self._visualizer.setVisible(False)

        self._test = value
        log.info("Set test: %s", self.test)

    def _on_open_clicked(self):
        filename, _ = qw.QFileDialog.getOpenFileName(
            self,
            "Cargar Registro",
            config.record_path,
            "Registro del OpenEOG (*.oeog)",
        )
        if filename:
            config.record_path = dirname(filename)
            study_name = basename(filename)

            self.study = load_study(filename)

            self.setWindowTitle(f"OpenEOG Editor - {study_name}")

    def _on_test_changed_index(self, index: int):
        self.test = self.study[index]
