#!/bin/bash
# run_backend.sh

# Get the absolute path to the project root
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$ROOT_DIR"

# 1. Activate Virtual Environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "[!] Virtual environment 'venv' not found. Please create it first."
    exit 1
fi

# 2. Set PYTHONPATH to the root directory
export PYTHONPATH="$ROOT_DIR:$PYTHONPATH"

# 3. Verify Dependencies
if ! python3 -c "import agno, openai, dotenv" 2>/dev/null; then
    echo "[!] Missing dependencies in venv. Installing..."
    pip install -r backend/requirements.txt
fi

# 4. Run the application
echo "[*] Launching MAAS Backend from $ROOT_DIR..."
python3 backend/main.py
