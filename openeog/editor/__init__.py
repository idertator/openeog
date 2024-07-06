import sys

from PySide6 import QtWidgets

from openeog.core import log

from .gui import MainWindow

VERSION = "1.0.0"


def main():
    log.info(
        "Starting OpenEOG Editor {version}".format(
            version=VERSION,
        )
    )

    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationDomain("diatax")
    app.setApplicationName("OpenEOG")
    app.setApplicationVersion(VERSION)
    app.setApplicationDisplayName("OpenEOG Editor")

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
