#!/bin/bash
set -e

# Project Root
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$PROJECT_ROOT/backend"

# Function to kill child processes on exit
cleanup() {
    echo "🛑 Shutting down backend..."
    kill $(jobs -p) 2>/dev/null
    exit
}
trap cleanup SIGINT SIGTERM

echo "🚀 Starting MAAS Backend Service"
echo "=================================="

# 1. Start Infrastructure (Docker)
echo "🐳 [1/2] Checking Database & Redis..."
docker-compose up -d db redis

# Wait a bit if we just started them
# We can be smarter, but sleep is safe
sleep 2

# 2. Start Backend (Local)
echo "🐍 [2/2] Starting Backend (Local Port 7777)..."

if [ -d "$PROJECT_ROOT/venv" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
elif [ -d "$BACKEND_DIR/venv" ]; then
    source "$BACKEND_DIR/venv/bin/activate"
else
    echo "⚠️  No venv found! Attempting system python..."
fi

export PYTHONPATH="$BACKEND_DIR"

# Run in foreground to see logs directly
python3 "$BACKEND_DIR/main.py"
