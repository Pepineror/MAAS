#!/bin/bash
set -e

# Project Root
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
UI_DIR="$PROJECT_ROOT/agent-ui"

cleanup() {
    echo "🛑 Shutting down UI..."
    exit
}
trap cleanup SIGINT SIGTERM

echo "🚀 Starting MAAS Agent UI"
echo "=================================="

echo "⚛️  Starting Agent UI (Local Port 3001)..."
cd "$UI_DIR"

# Ensure we have dependencies
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Agent UI dependencies..."
    npm install
fi

# Run in foreground
npm run dev -- -p 3001
