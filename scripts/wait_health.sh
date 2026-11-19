#!/usr/bin/env bash
# Чекає готовності сервісу з тайм-аутом. ./scripts/wait_health.sh [таймаут_сек]
set -u
TIMEOUT="${1:-60}"
URL="http://localhost:${PORT:-8000}/health"
end=$(( $(date +%s) + TIMEOUT ))
while [ "$(date +%s)" -lt "$end" ]; do
  # --max-time: один запит не може зависнути довше 3 с
  if curl -fsS --max-time 3 "$URL"; then echo; echo "health OK"; exit 0; fi
  sleep 2
done
echo "health FAILED: сервіс не відповів за ${TIMEOUT} с"
exit 1
