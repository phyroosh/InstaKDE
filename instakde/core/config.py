import os
from pathlib import Path

# Application Identity
APP_NAME = "InstaKDE"
APP_VERSION = "2.0.0"
APP_AUTHOR = "InstaKDE Project"
APP_ID = "io.github.instakde"
INSTAGRAM_URL = "https://www.instagram.com/"

# User-Agent - Mobile reference (Samsung Galaxy S20 Ultra)
USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 13; SM-G988B) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Mobile Safari/537.36"
)

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = BASE_DIR / "instakde" / "assets"
LOGO_SVG = ASSETS_DIR / "logo.svg"

HOME = Path.home()
XDG_DATA_HOME = Path(os.environ.get("XDG_DATA_HOME", HOME / ".local" / "share"))
XDG_CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config"))
XDG_CACHE_HOME = Path(os.environ.get("XDG_CACHE_HOME", HOME / ".cache"))

APP_DATA_DIR = XDG_DATA_HOME / "InstaKDE"
APP_CONFIG_DIR = XDG_CONFIG_HOME / "InstaKDE"
APP_CACHE_DIR = XDG_CACHE_HOME / "InstaKDE"

MEDIA_CACHE_DIR = APP_CACHE_DIR / "media"
COOKIE_STORE = APP_DATA_DIR / "cookies"
SESSION_DIR = APP_DATA_DIR / "session"
LOG_DIR = APP_DATA_DIR / "logs"

def ensure_dirs() -> None:
    for d in (APP_DATA_DIR, APP_CONFIG_DIR, APP_CACHE_DIR, MEDIA_CACHE_DIR, COOKIE_STORE, SESSION_DIR, LOG_DIR):
        d.mkdir(parents=True, exist_ok=True)
