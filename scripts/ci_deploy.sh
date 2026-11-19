#!/usr/bin/env bash
# Розгортання образу в навчальному середовищі (runner/VM) і перевірка /health.
# ./scripts/ci_deploy.sh ghcr.io/owner/devops-pr6:<sha>
set -euo pipefail
NEW="${1:?потрібен образ}"
cd "$(dirname "$0")/.."
echo "Розгортаю $NEW"
IMAGE="$NEW" docker compose up -d --no-build --force-recreate
./scripts/wait_health.sh 60
