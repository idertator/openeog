from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QFileDialog, QMainWindow, QMessageBox

from bsp.core.io import save_study

from . import icons  # noqa
from .plotter import Plotter
from .recorder import Recorder
from .screens import ScreensManager
from .settings import SettingsDialog
from .stimulator import Stimulator


class MainWindow(QMainWindow):
    def __init__(self, screens: ScreensManager):
        super().__init__()

        self.setWindowTitle("EOG Recorder")

        # Setup state
        self._recording = False

        # Setting toolbar
        self._toolbar = self.addToolBar("Main")
        self._toolbar.setMovable(False)

        # Setup dialogs
        self._settings_dialog = SettingsDialog(screens, self)

        # Setup actions
        self._settings_action = QAction(QIcon(":settings.svg"), "&SettingsDialog", self)
        self._settings_action.triggered.connect(self.on_settings_clicked)
        self._toolbar.addAction(self._settings_action)

        self._play_action = QAction(QIcon(":play.svg"), "&Play", self)
        self._play_action.triggered.connect(self.on_play_clicked)
        self._toolbar.addAction(self._play_action)

        self._stop_action = QAction(QIcon(":stop.svg"), "&Stop", self)
        self._stop_action.triggered.connect(self.on_stop_clicked)
        self._stop_action.setEnabled(False)
        self._toolbar.addAction(self._stop_action)

        self._plotter = Plotter(length=5000)
        self.setCentralWidget(self._plotter)

        self._stimulator = Stimulator(
            screens=screens,
            settings=self._settings_dialog,
        )

        self._recorder = Recorder(
            screens=screens,
            settings=self._settings_dialog,
            stimulator=self._stimulator,
            plotter=self._plotter,
            parent=self,
        )
        self._recorder.finished.connect(self.on_recording_finished)

    @Slot()
    def on_settings_clicked(self):
        self._settings_dialog.exec()

    @Slot()
    def on_play_clicked(self):
        self._recording = True
        self._stop_action.setEnabled(True)
        self._play_action.setEnabled(False)

        self._recorder.start()

    @Slot()
    def on_stop_clicked(self):
        self._recording = False
        self._stop_action.setEnabled(False)
        self._play_action.setEnabled(True)

    @Slot()
    def on_recording_finished(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Seleccione ruta de almacenamiento del estudio",
            None,
            "Estudio EOG del BioSignalPlux (*.bsp)",
        )

        if filepath:
            if not filepath.lower().endswith(".bsp"):
                filepath += ".bsp"

            study = self._recorder.build_study()
            save_study(study, filepath)
            QMessageBox.information(
                self,
                "Información",
                "Estudio almacenado satisfactoriamente en {filepath}".format(
                    filepath=filepath,
                ),
            )
