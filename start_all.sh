#!/bin/bash
set -e

# Project Root
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$PROJECT_ROOT/backend"
UI_DIR="$PROJECT_ROOT/agent-ui"

# Function to kill child processes on exit
cleanup() {
    echo "🛑 Shutting down services..."
    kill $(jobs -p) 2>/dev/null
    exit
}
trap cleanup SIGINT SIGTERM

echo "🚀 MAAS v4.0 Unified Startup Script"
echo "=================================="

# 1. Start Infrastructure (Docker)
echo "🐳 [1/3] Starting Database & Redis (Docker)..."
# Clean potential corrupted state first if needed, or just force recreate
docker-compose down --remove-orphans 2>/dev/null || true
docker-compose up -d db redis

# Wait for DB to be ready (dumb wait)
echo "⏳ Waiting 5s for DB to initialize..."
sleep 5

# 2. Start Backend (Local)
echo "🐍 [2/3] Starting Backend (Local Port 7777)..."
if [ -d "$PROJECT_ROOT/venv" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
    # Ensure dependencies
    # pip install -r "$BACKEND_DIR/requirements.txt" > /dev/null 2>&1 &
elif [ -d "$BACKEND_DIR/venv" ]; then
     source "$BACKEND_DIR/venv/bin/activate"
else
    echo "⚠️  No venv found! Attempting system python..."
fi

export PYTHONPATH="$BACKEND_DIR"
# Run in background and pipe logs
python3 "$BACKEND_DIR/main.py" > "$PROJECT_ROOT/backend.log" 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID). Logs: backend.log"

# 3. Start Agent UI (Local)
echo "⚛️  [3/3] Starting Agent UI (Local Port 3001)..."
cd "$UI_DIR"
# Ensure we have dependencies
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Agent UI dependencies..."
    npm install
fi

# Run in background
npm run dev -- -p 3001 > "$PROJECT_ROOT/agent-ui.log" 2>&1 &
UI_PID=$!
echo "✅ Agent UI started (PID: $UI_PID). Logs: agent-ui.log"

echo "=================================="
echo "🎉 System operational!"
echo "   - Backend: http://localhost:7777"
echo "   - Agent UI: http://localhost:3001"
echo "   - Press Ctrl+C to stop everything."
echo "=================================="

# Wait for processes
wait $BACKEND_PID $UI_PID
