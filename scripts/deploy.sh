#!/usr/bin/env bash
# Деплой вказаної версії: ./scripts/deploy.sh 1.1.0
set -euo pipefail
VER="${1:?вкажи версію, напр. 1.1.0}"
cd "$(dirname "$0")/.."

if [ -f .current_version ]; then cp .current_version .previous_version; fi

export APP_VERSION="$VER" IMAGE="pr6-service:$VER"
docker compose build
docker compose up -d

# чекаємо, поки сервіс відповість
./scripts/wait_health.sh 30 >/dev/null || true

if curl -fs --max-time 3 http://localhost:8000/version | grep -q "\"$VER\""; then
  echo "$VER" > .current_version
  echo "OK: працює версія $VER"
else
  echo "ПОМИЛКА: версія $VER не піднялась, відкат"
  ./scripts/rollback.sh
  exit 1
fi
