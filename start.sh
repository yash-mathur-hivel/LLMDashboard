#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

# ── 1. PostgreSQL ─────────────────────────────────────────────────────────────
echo "→ Checking PostgreSQL..."
if pg_isready -q; then
  echo "  PostgreSQL is already running."
else
  echo "  Starting PostgreSQL..."
  brew services start postgresql@17
  # Wait up to 10 s for it to accept connections
  for i in {1..10}; do
    pg_isready -q && break
    sleep 1
  done
  pg_isready -q || { echo "  ERROR: PostgreSQL failed to start."; exit 1; }
  echo "  PostgreSQL started."
fi

# ── 2. Backend ────────────────────────────────────────────────────────────────
echo "→ Starting backend (port 8000)..."
cd "$ROOT/backend"
../.venv/bin/uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
echo "  Backend PID: $BACKEND_PID"

# ── 3. Frontend ───────────────────────────────────────────────────────────────
echo "→ Starting frontend (port 5173)..."
cd "$ROOT/frontend"
npm run dev &
FRONTEND_PID=$!
echo "  Frontend PID: $FRONTEND_PID"

# ── Cleanup on exit ───────────────────────────────────────────────────────────
trap "echo ''; echo '→ Shutting down...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; wait" SIGINT SIGTERM

echo ""
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:5173"
echo "  API docs: http://localhost:8000/docs"
echo ""
echo "  Press Ctrl+C to stop."
echo ""

wait
