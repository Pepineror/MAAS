#!/bin/bash
set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$BACKEND_DIR/backend_env"

echo "🚀 Setting up environment for Full Workflow Test..."

# 1. Create Virtual Environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# 2. Activate Virtual Environment
source "$VENV_DIR/bin/activate"

# 3. Install Dependencies
echo "📦 Installing/Verifying dependencies..."
# We install the package in editable mode if possible or just the requirements
# Using pip to install requirements relative to backend root
pip install -r "$BACKEND_DIR/requirements.txt" || {
    echo "⚠️  Failed to install full requirements. Attempting to install minimal packages for the script..."
    pip install agno sqlalchemy asyncpg pydantic openai python-dotenv psycopg[binary] psycopg-pool regex python-redmine PyJWT pgvector
}

# 4. Run the Python Script
echo "▶️  Running test_full_workflow.py..."
export PYTHONPATH="$BACKEND_DIR/.."
python "$SCRIPT_DIR/test_full_workflow.py"

echo "✅ Test execution attempt finished."
