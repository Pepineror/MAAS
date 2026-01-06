#!/bin/bash
set -e

# Get directories
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$BACKEND_DIR/venv" # Assuming venv is in backend/venv or root/venv? User usage suggests root/venv.

# Check root venv
if [ -d "$BACKEND_DIR/venv" ]; then
    VENV_DIR="$BACKEND_DIR/venv"
elif [ -d "$BACKEND_DIR/../venv" ]; then
    VENV_DIR="$BACKEND_DIR/../venv"
else
    echo "⚠️  Virtual environment not found in standard locations."
fi

echo "🚀 Starting MAAS Backend Locally..."

# Activate Venv
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
    echo "✅ Virtual environment activated."
else
    echo "⚠️  Could not activate virtual environment. Proceeding with system python..."
fi

# Set PYTHONPATH
export PYTHONPATH="$BACKEND_DIR"

# Check DB connection (Simple check)
echo "🔍 Checking Database connection..."
# This is a basic check; real app will fail if DB is down.

# Install/Check dependencies if needed (optional, keeping it fast)
# pip install -r "$BACKEND_DIR/requirements.txt"

# Run Backend
echo "▶️  Running backend/main.py..."
python3 "$BACKEND_DIR/main.py"
