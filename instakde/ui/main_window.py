import logging
from PySide6.QtWidgets import (
    QWidget,
    QSystemTrayIcon,
    QMenu,
    QApplication,
)
from PySide6.QtGui import QIcon, QAction, QCloseEvent, QResizeEvent
from PySide6.QtCore import Qt

from instakde.core import config
from instakde.core.browser import InstagramBrowserView
from instakde.ui.theme import GLOBAL_STYLESHEET

log = logging.getLogger(__name__)


class MainWindow(QWidget):
    """
    Main desktop window for InstaKDE.
    Provides a centered, authentic mobile frame that prevents layout distortion.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(config.APP_NAME)
        self.resize(480, 860)
        self.setMinimumSize(360, 500)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        # Window icon
        app_icon = QIcon(str(config.LOGO_SVG))
        self.setWindowIcon(app_icon)

        # Core Browser View (parented to this widget, geometry managed in resizeEvent)
        self.browser = InstagramBrowserView(self)

        # System Tray Integration
        self._build_tray(app_icon)

        log.info("[SHELL] InstaKDE MainWindow initialized successfully")

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        # Keep Instagram in its native mobile layout (max 500px) centered horizontally
        # This prevents Instagram from breaking into the tablet sidebar or dropping the top '+' bar
        content_w = min(self.width(), 500)
        offset_x = (self.width() - content_w) // 2
        self.browser.setGeometry(offset_x, 0, content_w, self.height())

    def _build_tray(self, icon: QIcon) -> None:
        if not QSystemTrayIcon.isSystemTrayAvailable():
            self.tray = None
            return

        self.tray = QSystemTrayIcon(icon, self)
        self.tray.setToolTip(config.APP_NAME)

        menu = QMenu(self)

        show_act = QAction("Show InstaKDE", self)
        show_act.triggered.connect(self._toggle_visibility)
        menu.addAction(show_act)

        reload_act = QAction("Reload", self)
        reload_act.triggered.connect(self.browser.reload)
        menu.addAction(reload_act)

        menu.addSeparator()

        quit_act = QAction("Quit InstaKDE", self)
        quit_act.triggered.connect(QApplication.instance().quit)
        menu.addAction(quit_act)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

    def _toggle_visibility(self) -> None:
        if self.isVisible() and not self.isMinimized():
            self.hide()
        else:
            self.showNormal()
            self.activateWindow()

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self._toggle_visibility()

    def closeEvent(self, event: QCloseEvent) -> None:
        # If system tray is active, hide to tray instead of quitting
        if self.tray and self.tray.isVisible():
            self.hide()
            event.ignore()
        else:
            event.accept()
