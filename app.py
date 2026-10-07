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

def setup_environment():
    # 1. Preload full freeworld FFmpeg codecs (H.264 / HEVC) if available
    import ctypes
    candidate_codecs = [
        str(config.BASE_DIR / "build_tools" / "codecs" / "libavcodec.so.62"),
        "/usr/lib64/ffmpeg/libavcodec.so.62",
        "/usr/lib/ffmpeg/libavcodec.so.62",
    ]
    for cpath in candidate_codecs:
        if os.path.isfile(cpath):
            try:
                ctypes.CDLL(cpath, mode=ctypes.RTLD_GLOBAL)
                logging.getLogger("instakde").info(f"[CODECS] Preloaded full media codec from {cpath}")
                break
            except Exception as e:
                logging.getLogger("instakde").warning(f"[CODECS] Failed to preload {cpath}: {e}")

    # 2. Configure Chromium flags for video autoplay and hardware acceleration
    flags = [
        "--autoplay-policy=no-user-gesture-required",
        "--enable-features=VaapiVideoDecoder,CanvasOopRasterization",
    ]
    cur_flags = os.environ.get("QTWEBENGINE_CHROMIUM_FLAGS", "")
    for f in flags:
        if f not in cur_flags:
            cur_flags = f"{cur_flags} {f}".strip()
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = cur_flags


def main():
    setup_logging()
    setup_environment()

    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    app.setApplicationDisplayName(config.APP_NAME)
    app.setDesktopFileName("instakde")
    app.setWindowIcon(QIcon(str(config.LOGO_SVG)))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
