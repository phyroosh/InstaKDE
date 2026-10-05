# InstaKDE

> **A professional KDE Plasma desktop application for Instagram's mobile web experience.**

![KDE Plasma](https://img.shields.io/badge/KDE_Plasma-5%2B%2F6-blue?logo=kde&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-6.7%2B-green?logo=python&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Linux-294172?logo=linux)

---

## Overview

InstaKDE provides the complete, authentic Instagram mobile experience packaged inside a professional, lightweight KDE Plasma desktop window.

Rather than running fragile scrapers or maintaining separate custom frontends that fall out of sync with Meta's updates, InstaKDE leverages a dedicated, persistent Qt WebEngine environment configured with mobile touch capabilities and responsive reflow.

```
┌────────────────────────────────────────────────────────┐
│                        InstaKDE                        │
│                   (KDE Plasma Window)                  │
├────────────────────────────────────────────────────────┤
│                                                        │
│                    QWebEngineView                      │
│                          │                             │
│               Persistent QWebEngineProfile             │
│               (Mobile UA + Touch + Cookies)            │
│                          │                             │
│             Instagram Mobile Web Experience            │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Key Highlights
- **100% Authentic Instagram**: Direct access to Stories, Reels (with audio controls), Direct Messages, Explore, Search, and Post/Story creation.
- **Fluid Responsive Reflow**: Automatically reflows Instagram's layout from mobile phone aspect ratios (bottom tab bar) up to widescreen desktop layouts without scaling artifacts.
- **Persistent Session**: Log in once; authentication state and cookies persist cleanly in `~/.local/share/InstaKDE/session`.
- **KDE Desktop Integration**: Native window framing, desktop application identity (`org.kde.instakde`), system tray minimize/restore, and dark canvas aesthetic.
- **External Link Handling**: Non-Instagram links (links in bios, external sites) open directly in your default system web browser.
- **Keyboard Shortcuts**:
  - `F5` / `Ctrl+R`: Reload
  - `Ctrl+Shift+R`: Hard reload (bypass cache)
  - `Alt+Left` / `Alt+Right`: Back / Forward history
  - `Ctrl++` / `Ctrl+-`: Zoom in / Zoom out
  - `Ctrl+0`: Reset zoom

---

## Directory Structure

```
Instagram/
├── app.py                      # Application launcher & KDE app configuration
├── instakde/
│   ├── assets/
│   │   └── logo.svg            # Official vector icon
│   ├── core/
│   │   ├── config.py           # Identity, paths, and mobile User-Agent
│   │   └── browser.py          # Responsive InstagramBrowserView & WebEnginePage
│   └── ui/
│       ├── main_window.py      # Desktop shell, window geometry & system tray
│       └── theme.py            # Dark glass styles & scrollbar aesthetics
├── instakde.desktop            # FreeDesktop desktop launcher
└── requirements.txt            # Python dependencies
```

---

## Quick Start

### 1. Requirements
- Python 3.11+
- PySide6 6.7+ (including `QtWebEngineWidgets`)

On Fedora:
```bash
sudo dnf install python3-pyside6 python3-pyside6-addons qt6-qtwebengine
```

Or via pip:
```bash
pip install -r requirements.txt
```

### 2. Launch directly with Python
```bash
python3 app.py
```

### 3. Portable AppImage (No dependencies required)
A fully self-contained AppImage is available:
```bash
./InstaKDE-x86_64.AppImage
```

To build a fresh AppImage at any time:
```bash
./package_appimage.sh
```

### 4. Desktop Installation
To register InstaKDE in your KDE application launcher:
```bash
cp ~/.local/share/applications/org.kde.instakde.desktop ~/.local/share/applications/
```

---

## License

MIT
