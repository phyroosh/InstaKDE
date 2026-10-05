#!/usr/bin/env bash
set -e

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

echo "=== Step 1: Compiling InstaKDE binary with PyInstaller ==="
rm -rf build dist AppDir

.build_venv/bin/pyinstaller \
    --name instakde \
    --onedir \
    --windowed \
    --clean \
    --noconfirm \
    --add-data "instakde/assets:instakde/assets" \
    --collect-all PySide6 \
    app.py

echo "=== Step 2: Assembling AppDir structure ==="
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/icons/hicolor/scalable/apps
mkdir -p AppDir/usr/share/applications

# Copy compiled executable and PySide6/Qt resources
cp -r dist/instakde/* AppDir/usr/bin/

# Copy icons and desktop entry
cp instakde/assets/logo.svg AppDir/usr/share/icons/hicolor/scalable/apps/instakde.svg
cp instakde/assets/logo.svg AppDir/instakde.svg

cat << 'EOF' > AppDir/instakde.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=InstaKDE
GenericName=Instagram Client
Comment=A professional KDE desktop client for Instagram
Exec=instakde
Icon=instakde
Terminal=false
StartupWMClass=InstaKDE
Categories=Network;InstantMessaging;
Keywords=instagram;social;photos;reels;stories;direct;
EOF

cp AppDir/instakde.desktop AppDir/usr/share/applications/

# Create AppRun launcher with exact PySide6 6.11 QtWebEngine paths
cat << 'EOF' > AppDir/AppRun
#!/bin/sh
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/bin/_internal:${HERE}/usr/bin:${LD_LIBRARY_PATH}"
export QTWEBENGINE_DISABLE_SANDBOX=1
export QT_PLUGIN_PATH="${HERE}/usr/bin/_internal/PySide6/Qt/plugins"
export QTWEBENGINE_RESOURCES_PATH="${HERE}/usr/bin/_internal/PySide6/Qt/resources"
export QTWEBENGINE_LOCALES_PATH="${HERE}/usr/bin/_internal/PySide6/Qt/translations/qtwebengine_locales"
exec "${HERE}/usr/bin/instakde" "$@"
EOF
chmod +x AppDir/AppRun

echo "=== Step 3: Generating AppImage ==="
rm -f InstaKDE-x86_64.AppImage
ARCH=x86_64 ./build_tools/appimagetool AppDir InstaKDE-x86_64.AppImage

echo "=== Build Complete: InstaKDE-x86_64.AppImage ==="
ls -lh InstaKDE-x86_64.AppImage
