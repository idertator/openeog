import sys

from PySide6 import QtWidgets

from openeog.core import log

from .gui import MainWindow, ScreensManager

VERSION = "1.1.0"


def main():
    log.info("Starting OpenEOG Recorder {version}".format(version=VERSION))

    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationDomain("idertator")
    app.setApplicationName("OpenEOG")
    app.setApplicationVersion(VERSION)
    app.setApplicationDisplayName("OpenEOG Recorder")

    screens = ScreensManager(app)

    window = MainWindow(screens)
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
