#!/bin/bash
# Auto pull and deployment synchronization script for Luka Mosala SaaS

set -e

echo "[Luka Mosala] Starting git pull synchronization..."

git fetch origin
git pull origin $(git rev-parse --abbrev-ref HEAD)

if [ -f "backend/manage.py" ]; then
    echo "[Luka Mosala] Running backend migrations..."
    python backend/manage.py migrate --noinput
fi

echo "[Luka Mosala] Synchronization complete!"
