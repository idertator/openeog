from PySide6.QtGui import QAction, QIcon, QShowEvent
from PySide6.QtWidgets import QFileDialog, QMainWindow, QMessageBox

from bsp.core import Protocol, Session, log, saccadic_report, save_study

from . import resources  # noqa
from .newrecord import NewRecordWizard
from .plotter import Plotter
from .recorder import Recorder
from .screens import ScreensManager
from .settings import SettingsDialog
from .stimulator import Stimulator


class MainWindow(QMainWindow):
    def __init__(self, screens: ScreensManager):
        super().__init__()
        self._screens = screens

        self.setWindowTitle("EOG Recorder")

        # Setup state
        self._recording = False

        # Setting toolbar
        self._toolbar = self.addToolBar("Main")
        self._toolbar.setMovable(False)

        # Setup dialogs
        self._settings_dialog = SettingsDialog(screens, self)

        # Setup actions
        self._settings_action = QAction(QIcon(":settings.svg"), "&Configuración", self)
        self._settings_action.triggered.connect(self.on_settings_clicked)
        self._toolbar.addAction(self._settings_action)

        self._play_action = QAction(QIcon(":play.svg"), "&Grabar", self)
        self._play_action.triggered.connect(self.on_play_clicked)
        self._toolbar.addAction(self._play_action)

        self._stop_action = QAction(QIcon(":stop.svg"), "&Parar", self)
        self._stop_action.triggered.connect(self.on_stop_clicked)
        self._stop_action.setEnabled(False)
        self._toolbar.addAction(self._stop_action)

        self._plotter = Plotter(
            length=5000,
            resolution=self._settings_dialog.resolution,
        )
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

        self._new_record_wizard = None
        self._session = None

    def showEvent(self, event: QShowEvent):
        if not self._new_record_wizard:
            self._new_record_wizard = NewRecordWizard(self._screens, self)
            self._new_record_wizard.exec()

        self._session = self._new_record_wizard.session

    def on_settings_clicked(self):
        self._settings_dialog.exec()

    def on_play_clicked(self):
        self._recording = True
        self._stop_action.setEnabled(True)
        self._play_action.setEnabled(False)

        self._recorder.start(self._session)

    def on_stop_clicked(self):
        self._recording = False
        self._stop_action.setEnabled(False)
        self._play_action.setEnabled(True)

    def on_recording_finished(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Seleccione ruta de almacenamiento del estudio",
            None,
            "Estudio EOG del BioSignalPlux (*.bsp)",
        )

        if filepath:
            if "." in filepath:
                filepath = ".".join(filepath.split(".")[:-1])

            study = self._recorder.build_study()
            save_study(study, filepath + ".bsp")

            if study.protocol == Protocol.Saccadic:
                saccadic_report(study, filepath + ".xlsx")
                msg = """Estudio almacenado satisfactoriamente en {study_path} y
                      reporte sacádico en {report_path}""".format(
                    study_path=filepath + ".bsp",
                    report_path=filepath + ".xlsx",
                )
            else:
                msg = "Estudio almacenado satisfactoriamente en {study_path}".format(
                    study_path=filepath + ".bsp",
                )

            QMessageBox.information(self, "Información", msg)
