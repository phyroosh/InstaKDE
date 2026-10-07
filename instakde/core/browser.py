import logging
from typing import Optional
from PySide6.QtCore import Qt, QUrl, QTimer, Slot
from PySide6.QtGui import QColor, QDesktopServices, QKeySequence, QShortcut
from PySide6.QtWebEngineCore import (
    QWebEngineProfile,
    QWebEngineSettings,
    QWebEnginePage,
)
from PySide6.QtWebEngineWidgets import QWebEngineView

from instakde.core import config

log = logging.getLogger(__name__)

ALLOWED_HOSTS = (
    "instagram.com",
    "facebook.com",
    "fbcdn.net",
    "cdninstagram.com",
    "threads.net",
    "meta.com",
)

POPUP_DISMISS_JS = """
(() => {
    try {
        let all = Array.from(document.querySelectorAll('*'));
        // 1. "Save your login info" modal -> click Save or Not now
        let notNow = all.find(el => el.innerText && el.innerText.trim() === 'Not now');
        let save = all.find(el => el.innerText && el.innerText.trim() === 'Save');
        let target = save || notNow;
        if (target) {
            let clickable = target.closest('button, [role="button"]') || target;
            clickable.click();
            return 'dismissed: ' + target.innerText.trim();
        }
        // 2. Notification prompt -> click Cancel or Not Now
        let cancel = all.find(el => el.innerText && (el.innerText.trim() === 'Cancel' || el.innerText.trim().toLowerCase() === 'not now'));
        if (cancel) {
            let clickable = cancel.closest('button, [role="button"]') || cancel;
            clickable.click();
            return 'dismissed: ' + cancel.innerText.trim();
        }
    } catch(e) {}
    return 'none';
})()
"""

_session_profile: Optional[QWebEngineProfile] = None

def get_session_profile() -> QWebEngineProfile:
    """Returns the persistent QWebEngineProfile for InstaKDE."""
    global _session_profile
    if _session_profile is None:
        config.ensure_dirs()
        _session_profile = QWebEngineProfile("InstaKDESession")
        _session_profile.setCachePath(str(config.APP_CACHE_DIR / "webcache"))
        _session_profile.setPersistentStoragePath(str(config.SESSION_DIR))
        _session_profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies
        )
        _session_profile.setHttpUserAgent(config.USER_AGENT)

        settings = _session_profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.TouchEventsApiEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanPaste, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)

    return _session_profile


class InstagramWebPage(QWebEnginePage):
    """
    Custom WebEnginePage that:
    - Sets a dark background color to prevent white flashes
    - Suppresses harmless Chromium Permissions-Policy header warnings from terminal
    - Safely opens external http/https links in the system default browser
    - Handles target="_blank" window creation within the same page
    """

    def __init__(self, profile: QWebEngineProfile, parent: Optional[QWebEngineView] = None):
        super().__init__(profile, parent)
        self.setBackgroundColor(QColor(0, 0, 0))

    def javaScriptConsoleMessage(
        self,
        level: QWebEnginePage.JavaScriptConsoleMessageLevel,
        message: str,
        line_number: int,
        source_id: str
    ) -> None:
        # Filter out noisy Permissions-Policy header warnings from cluttering terminal
        if "Permissions-Policy" in message:
            return
        log.debug(f"[JS {level.name}] {source_id}:{line_number} -> {message}")

    def acceptNavigationRequest(
        self,
        url: QUrl,
        nav_type: QWebEnginePage.NavigationType,
        is_main_frame: bool
    ) -> bool:
        scheme = url.scheme().lower()

        # Ignore mobile app intent:// schemes to prevent system handler errors
        if scheme == "intent":
            log.info(f"[BROWSER] Ignored mobile intent scheme: {url.toString()}")
            return False

        # Handle external HTTP/HTTPS links
        if scheme in ("http", "https"):
            host = url.host().lower()
            if nav_type == QWebEnginePage.NavigationType.NavigationTypeLinkClicked:
                if not self._is_internal_host(host):
                    log.info(f"[BROWSER] Opening external link in system browser: {url.toString()}")
                    QDesktopServices.openUrl(url)
                    return False

        return super().acceptNavigationRequest(url, nav_type, is_main_frame)

    def createWindow(self, win_type: QWebEnginePage.WebWindowType) -> QWebEnginePage:
        # Redirect new tab / new window creations into this same page
        log.info(f"[BROWSER] Handling window creation (type={win_type}) in current view")
        return self

    @staticmethod
    def _is_internal_host(host: str) -> bool:
        if not host:
            return True
        for allowed in ALLOWED_HOSTS:
            if host == allowed or host.endswith("." + allowed):
                return True
        return False


class InstagramBrowserView(QWebEngineView):
    """
    Dedicated responsive Instagram mobile web view.
    Maintains authentic mobile rendering without injected synthetic buttons.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._profile = get_session_profile()
        self._page = InstagramWebPage(self._profile, self)
        self.setPage(self._page)

        # Style with dark background to avoid white flashes
        self.setStyleSheet("background-color: #000000;")

        self._setup_shortcuts()
        self._setup_events()

        # Load Instagram mobile web
        log.info(f"[BROWSER] Loading Instagram from {config.INSTAGRAM_URL}")
        self.load(QUrl(config.INSTAGRAM_URL))

    def _setup_shortcuts(self) -> None:
        # F5 / Ctrl+R: Reload
        QShortcut(QKeySequence("F5"), self, activated=self.reload)
        QShortcut(QKeySequence("Ctrl+R"), self, activated=self.reload)
        QShortcut(
            QKeySequence("Ctrl+Shift+R"),
            self,
            activated=lambda: self.page().triggerAction(QWebEnginePage.WebAction.ReloadAndBypassCache)
        )

        # Navigation: Alt+Left (Back), Alt+Right (Forward)
        QShortcut(QKeySequence("Alt+Left"), self, activated=self.back)
        QShortcut(QKeySequence("Alt+Right"), self, activated=self.forward)

        # Zoom controls
        QShortcut(QKeySequence("Ctrl+="), self, activated=self._zoom_in)
        QShortcut(QKeySequence("Ctrl++"), self, activated=self._zoom_in)
        QShortcut(QKeySequence("Ctrl+-"), self, activated=self._zoom_out)
        QShortcut(QKeySequence("Ctrl+0"), self, activated=self._zoom_reset)

    def _setup_events(self) -> None:
        self.loadFinished.connect(self._on_load_finished)

    @Slot(bool)
    def _on_load_finished(self, ok: bool) -> None:
        log.info(f"[BROWSER] Page load finished (ok={ok})")
        if ok:
            # Trigger popup dismissal after delays to handle post-load prompts
            QTimer.singleShot(1500, self._dismiss_popups)
            QTimer.singleShot(4000, self._dismiss_popups)
            QTimer.singleShot(8000, self._dismiss_popups)

    def _dismiss_popups(self) -> None:
        def on_dismissed(result):
            if result and result != "none":
                log.info(f"[BROWSER] Modal auto-dismiss: {result}")
        self.page().runJavaScript(POPUP_DISMISS_JS, on_dismissed)

    def _zoom_in(self) -> None:
        self.setZoomFactor(min(2.5, self.zoomFactor() + 0.1))

    def _zoom_out(self) -> None:
        self.setZoomFactor(max(0.5, self.zoomFactor() - 0.1))

    def _zoom_reset(self) -> None:
        self.setZoomFactor(1.0)

    def closeEvent(self, event) -> None:
        self.setPage(None)
        super().closeEvent(event)
