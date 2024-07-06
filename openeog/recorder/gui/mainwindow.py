from os.path import join

from PySide6.QtGui import QAction, QIcon, QShowEvent
from PySide6.QtWidgets import QMainWindow, QMessageBox

from openeog.core import Session, log, save_study

from . import resources  # noqa
from .newrecord import NewRecordWizard
from .plotter import Plotter
from .recorder import Recorder
from .screens import ScreensManager
from .stimulator import Stimulator


class MainWindow(QMainWindow):
    def __init__(self, screens: ScreensManager):
        super().__init__()
        self._screens = screens

        self.setWindowTitle("EOG Recorder")

        # Setup state
        self._recording = False
        self._stopped = False

        # Setting toolbar
        self._toolbar = self.addToolBar("Main")
        self._toolbar.setMovable(False)

        # Setup actions
        self._play_action = QAction(QIcon(":play.svg"), "&Grabar", self)
        self._play_action.triggered.connect(self.on_play_clicked)
        self._toolbar.addAction(self._play_action)

        self._stop_action = QAction(QIcon(":stop.svg"), "&Parar", self)
        self._stop_action.triggered.connect(self.on_stop_clicked)
        self._stop_action.setEnabled(False)
        self._toolbar.addAction(self._stop_action)

        self._plotter = Plotter(
            length=5000,
        )
        self.setCentralWidget(self._plotter)

        self._stimulator: Stimulator | None = None
        self._recorder: Recorder | None = None

        self._new_record_wizard = None
        self._session: Session | None = None

    @property
    def recorder(self) -> Recorder:
        if not self._recorder:
            self._stimulator = Stimulator(
                screens=self._screens,
            )

            self._recorder = Recorder(
                screens=self._screens,
                stimulator=self._stimulator,
                plotter=self._plotter,
                parent=self,
            )
            self._recorder.finished.connect(self.on_recording_finished)

        return self._recorder

    def showEvent(self, event: QShowEvent):
        if not self._new_record_wizard:
            self._new_record_wizard = NewRecordWizard(self._screens, self)
            self._new_record_wizard.exec()

        self._session = self._new_record_wizard.session

    def _set_stopped_state(self):
        self._stop_action.setEnabled(False)
        self._play_action.setEnabled(True)

    def on_play_clicked(self):
        self._recording = True
        self._stop_action.setEnabled(True)
        self._play_action.setEnabled(False)

        self.recorder.start(self._session)

    def on_stop_clicked(self):
        self._stopped = True
        self._recorder.stop()
        self._recording = False
        self._set_stopped_state()

    def on_recording_finished(self):
        self._set_stopped_state()

        if self._stopped:
            return

        filepath = join(
            self._session.path,
            "{name}.oeog".format(
                name=self._session.name.replace(" ", "_"),
            ),
        )

        study = self.recorder.build_study()
        save_study(study, filepath)

        if error_rate := study.error_rate:
            msg = "Estudio almacenado satisfactoriamente en {filepath} con una tasa de error de {rate:.4f}%".format(
                filepath=filepath,
                rate=error_rate,
            )
        else:
            msg = "Estudio almacenado satisfactoriamente en {filepath}".format(
                filepath=filepath,
            )

        log.info(msg)
        QMessageBox.information(self, "Información", msg)
