#!/usr/bin/env bash
set -e

echo "========================================"
echo "  Parik24 Live Football Scraper"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] Python3 not found! Install Python 3.11+"
    exit 1
fi

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "[1/3] Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install dependencies if not installed
if ! pip show parik-live-scraper &>/dev/null; then
    echo "[2/3] Installing dependencies..."
    pip install -e . > /dev/null 2>&1
    echo "Done!"
else
    echo "[2/3] Dependencies already installed."
fi

echo "[3/3] Fetching live football matches..."
echo

parik-live

echo
echo "========================================"
echo
echo "Commands you can try:"
echo "  parik-live                     - all live matches (table)"
echo "  parik-live --json              - JSON format"
echo "  parik-live --live-only         - only matches in play"
echo '  parik-live --league "Бразилія" - filter by league'
echo
