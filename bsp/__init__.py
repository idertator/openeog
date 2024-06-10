import sys

from PySide6.QtWidgets import QApplication

from bsp.core import log

from .gui import MainWindow, ScreensManager

VERSION = "1.1.0"


def main():
    log.info("Starting BSP {version}".format(version=VERSION))

    app = QApplication(sys.argv)
    app.setOrganizationDomain("idertator")
    app.setApplicationName("bsp")
    app.setApplicationVersion(VERSION)
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
