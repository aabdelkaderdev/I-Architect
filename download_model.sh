#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# download_model.sh — Download and extract ARLO embedding models
# ──────────────────────────────────────────────────────────────
# Downloads models.7z from Google Drive and extracts it into arlo/
#
# Prerequisites:
#   - pip install gdown
#   - 7z  (p7zip-full on Debian/Ubuntu, p7zip on Arch)
#
# Usage:
#   chmod +x download_model.sh
#   ./download_model.sh
# ──────────────────────────────────────────────────────────────

set -euo pipefail

GDRIVE_FILE_ID="1bQNQgDd-O8bb1XCuT0T9Ji-YYKqtH9Or"
ARCHIVE_NAME="models.7z"
EXTRACT_DIR="."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

# ── Dependency checks ────────────────────────────────────────
if ! command -v 7z &>/dev/null; then
    echo "❌  7z not found. Install it:"
    echo "    Ubuntu/Debian : sudo apt install p7zip-full"
    echo "    Arch          : sudo pacman -S p7zip"
    echo "    macOS         : brew install p7zip"
    exit 1
fi

if ! command -v gdown &>/dev/null; then
    echo "📦  gdown not found — installing via pip..."
    pip install --quiet gdown
fi

# ── Download ─────────────────────────────────────────────────
if [ -f "$ARCHIVE_NAME" ]; then
    echo "✅  $ARCHIVE_NAME already exists, skipping download."
else
    echo "⬇️   Downloading $ARCHIVE_NAME from Google Drive..."
    gdown --id "$GDRIVE_FILE_ID" -O "$ARCHIVE_NAME"
fi

# ── Extract ──────────────────────────────────────────────────
echo "📂  Extracting $ARCHIVE_NAME into $EXTRACT_DIR/ ..."
7z x "$ARCHIVE_NAME" -o"$EXTRACT_DIR" -aoa -y

echo ""
echo "✅  Done! Models extracted to $EXTRACT_DIR/models/"
