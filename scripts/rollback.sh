#!/usr/bin/env bash
# Відкат на попередню версію (образ уже є локально, перезбірка не потрібна)
set -euo pipefail
cd "$(dirname "$0")/.."
PREV="$(cat .previous_version 2>/dev/null || echo 1.0.0)"
echo "Відкат на версію $PREV"
export APP_VERSION="$PREV"
docker compose up -d --no-build
sleep 3
curl -fs http://localhost:8000/version && echo
echo "$PREV" > .current_version
