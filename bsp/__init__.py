import sys

from PySide6.QtWidgets import QApplication

from .gui import MainWindow, ScreensManager


def main():
    app = QApplication(sys.argv)
    app.setOrganizationDomain("idertator")
    app.setApplicationName("bsp")
    app.setApplicationVersion("1.0.2")
    app.setApplicationDisplayName("BioSignalPlux - EOG Recorder")

    screens = ScreensManager(app)

    window = MainWindow(screens)
    window.showMaximized()

    # Código Sofi
    # from .gui.protocols import AntisaccadicProtocolEditor
    # window = AntisaccadicProtocolEditor()
    # window.showMaximized()
    #
    # Código Alison
    # from .gui.protocols import PursuitProtocolEditor
    # window = PursuitProtocolEditor()
    # window.showMaximized()
    #
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
