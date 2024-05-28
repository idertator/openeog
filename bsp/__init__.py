import sys

from PySide6.QtWidgets import QApplication

from .gui import MainWindow, ScreensManager
from .gui.protocols import AntisaccadicProtocolEditor, PursuitProtocolEditor


def main():
    app = QApplication(sys.argv)
    app.setOrganizationDomain("idertator")
    app.setApplicationName("bsp")
    app.setApplicationVersion("1.0.2")
    app.setApplicationDisplayName("BioSignalPlux - EOG Recorder")

    # screens = ScreensManager(app)

    # TODO: Para probar su widget, reemplacen el window por el widget vuestro
    # window = MainWindow(screens)
    # window.showMaximized()

    # Código Sofi
    window = AntisaccadicProtocolEditor()
    window.showMaximized()

    # Código Alison
    window = PursuitProtocolEditor()
    window.showMaximized()

    sys.exit(app.exec())
