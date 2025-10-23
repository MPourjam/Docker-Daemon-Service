#!/bin/bash
set -euo pipefail

echo "[celery-entrypoint] Installing Python dependencies..."
pip install -q celery docker redis

echo "[celery-entrypoint] Starting Celery worker + beat..."
# Start both Celery worker and Celery Beat in the same container
# Trap ensures both die cleanly on SIGTERM (e.g., docker stop)
trap 'pkill -TERM -P $$ || true; wait' TERM INT

celery -A tasks worker -l info &
celery -A tasks beat   -l info &
wait -n                # wait until one process exits
pkill -TERM -P $$ || true
wait
