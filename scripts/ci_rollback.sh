#!/usr/bin/env bash
# Автоматичний відкат на останній перевірений образ (тег stable).
# ./scripts/ci_rollback.sh ghcr.io/owner/devops-pr6
set -uo pipefail
REPO="${1:?потрібна назва образу без тегу}"
cd "$(dirname "$0")/.."
if ! docker pull "$REPO:stable"; then
  echo "Попереднього стабільного образу немає, відкотитись нема на що"
  exit 1
fi
echo "Відкат на $REPO:stable"
IMAGE="$REPO:stable" docker compose up -d --no-build --force-recreate
./scripts/wait_health.sh 60
