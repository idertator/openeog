from PySide6.QtGui import QAction, QIcon, QShowEvent
from PySide6.QtWidgets import QMainWindow, QMessageBox
from bsp.core import Session, log, save_study
from os.path import join

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

        self._stimulator = Stimulator(
            screens=screens,
        )

        self._recorder = Recorder(
            screens=screens,
            stimulator=self._stimulator,
            plotter=self._plotter,
            parent=self,
        )
        self._recorder.finished.connect(self.on_recording_finished)

        self._new_record_wizard = None
        self._session: Session | None = None

    def showEvent(self, event: QShowEvent):
        if not self._new_record_wizard:
            self._new_record_wizard = NewRecordWizard(self._screens, self)
            self._new_record_wizard.exec()

        self._session = self._new_record_wizard.session

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
        filepath = join(
            self._session.path,
            "{name}.bsp".format(
                name=self._session.name.replace(" ", "_"),
            ),
        )

        study = self._recorder.build_study()
        save_study(study, filepath)

        msg = f"Estudio almacenado satisfactoriamente en {filepath}"

        log.info(msg)
        QMessageBox.information(self, "Información", msg)
