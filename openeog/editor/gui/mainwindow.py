from PySide6 import QtGui as qg
from PySide6 import QtWidgets as qw

from openeog.core import models


class MainWindow(qw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OpenEOG Editor")

        self.study: models.Study | None = None

        # Create the toolbar
        self._toolbar = self.addToolBar("Main")
        self._toolbar.setMovable(False)

        action_button = qg.QAction("&Abrir Estudio", self)
        self._toolbar.addAction(action_button)

        self._combo_container = qw.QWidget()
        self._combo_layout = qw.QHBoxLayout()
        self._combo_layout.setContentsMargins(0, 0, 0, 0)

        spacer = qw.QSpacerItem(
            40,
            20,
            qw.QSizePolicy.Expanding,
            qw.QSizePolicy.Minimum,
        )
        self._combo_layout.addItem(spacer)

        combo_box = qw.QComboBox()
        combo_box.addItems(["Option 1", "Option 2", "Option 3"])
        combo_box.setSizePolicy(
            qw.QSizePolicy.Minimum,
            qw.QSizePolicy.Minimum,
        )

        self._combo_layout.addWidget(combo_box)
        self._combo_container.setLayout(self._combo_layout)

        self._toolbar.addWidget(self._combo_container)

        self.setCentralWidget(qw.QWidget())
