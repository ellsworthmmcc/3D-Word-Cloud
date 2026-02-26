#!/usr/bin/env bash
set -e

if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Try: brew install python@3.12"
    exit 1
fi

echo "--- Setting up Backend ---"
(
  cd backend

  python3 -m venv .venv
  ./.venv/bin/pip install --upgrade pip
  
  if [ -f "requirements.txt" ]; then
    ./.venv/bin/pip install -r requirements.txt
  else
    ./.venv/bin/pip install -e .
  fi
)

echo "--- Setting up Frontend ---"
(
  cd frontend

  npm install
)


trap 'kill $(jobs -p)' EXIT

echo "--- Launching (Press Ctrl+C to stop both) ---"

./backend/.venv/bin/uvicorn backend.main:app --reload --port 8000 &

(cd frontend && npm run dev) &

wait