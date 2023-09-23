import sys

from PySide6.QtWidgets import QApplication

from .gui import MainWindow, ScreensManager


def main():
    app = QApplication(sys.argv)
    app.setOrganizationDomain("idertator")
    app.setApplicationName("bsp")
    app.setApplicationVersion("1.0.0")
    app.setApplicationDisplayName("BioSignalPlux - EOG Recorder")

    screens = ScreensManager(app)

    window = MainWindow(screens)
    window.showMaximized()

    sys.exit(app.exec())
