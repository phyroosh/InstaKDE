"""
InstaKDE Theme System
Premium Dark Glass Aesthetic
"""

DARK_CANVAS = "#0A0A0C"       # Deep charcoal background
GLASS_SURFACE = "rgba(255, 255, 255, 0.05)" # Translucent surface
GLASS_HOVER = "rgba(255, 255, 255, 0.1)"    # Interactive hover
GLASS_ACTIVE = "rgba(255, 255, 255, 0.15)"  # Active selection
BORDER_SOFT = "rgba(255, 255, 255, 0.08)"   # Subtle borders
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#8E8E93"    # Muted gray

GLOBAL_STYLESHEET = f"""
/* Base Application Style */
QWidget {{
    background-color: {DARK_CANVAS};
    color: {TEXT_PRIMARY};
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Noto, sans-serif;
    font-size: 14px;
}}

/* Exception for WebEngineView so it renders its own background */
QWebEngineView {{
    background-color: transparent;
}}

/* Scrollbars - Ultra minimal */
QScrollBar:vertical {{
    background: transparent;
    width: 6px;
    margin: 0px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER_SOFT};
    border-radius: 3px;
    min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{
    background: {GLASS_HOVER};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical, 
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
    border: none;
}}

/* QSplitter */
QSplitter::handle {{
    background-color: {BORDER_SOFT};
    width: 1px;
}}

/* QListWidget / QTreeWidget */
QListWidget {{
    background: transparent;
    border: none;
    outline: none;
}}
QListWidget::item {{
    padding: 12px;
    border-radius: 8px;
    margin: 4px;
}}
QListWidget::item:hover {{
    background-color: {GLASS_SURFACE};
}}
QListWidget::item:selected {{
    background-color: {GLASS_ACTIVE};
    color: {TEXT_PRIMARY};
}}

/* Inputs */
QLineEdit, QTextEdit {{
    background-color: {GLASS_SURFACE};
    border: 1px solid {BORDER_SOFT};
    border-radius: 8px;
    padding: 12px;
    color: {TEXT_PRIMARY};
}}
QLineEdit:focus, QTextEdit:focus {{
    border: 1px solid rgba(255, 255, 255, 0.3);
    background-color: {GLASS_HOVER};
}}

/* Progress Bar */
QProgressBar {{
    background-color: {GLASS_SURFACE};
    border: none;
    border-radius: 4px;
    text-align: center;
    color: transparent;
}}
QProgressBar::chunk {{
    background-color: {TEXT_PRIMARY};
    border-radius: 4px;
}}

/* Menus & Context Menus */
QMenu {{
    background-color: #1A1A1D;
    border: 1px solid {BORDER_SOFT};
    border-radius: 8px;
    padding: 4px;
}}
QMenu::item {{
    padding: 8px 24px 8px 12px;
    border-radius: 4px;
    color: {TEXT_PRIMARY};
}}
QMenu::item:selected {{
    background-color: {GLASS_ACTIVE};
}}

/* Dialogs */
QDialog {{
    background-color: {DARK_CANVAS};
}}

/* ToolTips */
QToolTip {{
    background-color: #1A1A1D;
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_SOFT};
    border-radius: 4px;
    padding: 4px;
}}
"""
