import os
import sys
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from instakde.core import config
from instakde.ui.main_window import MainWindow

def setup_logging():
    config.ensure_dirs()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stderr),
            logging.FileHandler(config.LOG_DIR / "instakde.log", encoding="utf-8")
        ]
    )

def main():
    setup_logging()

    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    app.setApplicationDisplayName(config.APP_NAME)
    app.setDesktopFileName("org.kde.instakde")
    app.setWindowIcon(QIcon(str(config.LOGO_SVG)))
    app.setQuitOnLastWindowClosed(False)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
