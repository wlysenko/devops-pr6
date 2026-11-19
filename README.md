# ПР6 — автоматизоване тестування та розгортання Python-сервісу

Сервіс на Flask з маршрутами `/health` і `/version`, Docker Compose, pytest, Testinfra, GitHub Actions, автоматичний відкат.

## Налаштування
```bash
cp .env.example .env            # APP_VERSION, APP_ENV, PORT, IMAGE
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
```

## Запуск
```bash
./scripts/deploy.sh 1.0.0        # збірка образу pr6-service:1.0.0 і запуск
curl localhost:8000/health
curl localhost:8000/version
```

## Перевірка
```bash
.venv/bin/pytest tests/test_app.py                                               # модульні тести
APP_VERSION=1.0.0 .venv/bin/pytest tests/test_infra.py --hosts=docker://pr6-service  # Testinfra
./scripts/wait_health.sh 60                                                      # очікування готовності з тайм-аутом
```

## Відкат
Локально:
```bash
./scripts/deploy.sh 1.1.0        # нова версія
./scripts/rollback.sh            # повернення на попередню (без перезбірки)
```
У CI: образ тегується хешем коміту (`ghcr.io/wlysenko/devops-pr6:<sha>`), останній перевірений образ має тег `stable`.
Якщо `/health` або Testinfra падає після розгортання, крок `Automatic rollback` запускає `scripts/ci_rollback.sh`,
піднімає `:stable`, повторно перевіряє `/health`, а запуск лишається позначеним як невдалий.

## CI/CD (`.github/workflows/ci-cd.yml`)
- pull request: `test` (pytest) → `build` (збірка образу)
- push у main: `test` → `build` + push в GHCR → `deploy` (розгортання, /health, Testinfra, тег stable)
- артефакти завжди: `unit-test-report` (JUnit XML), `deploy-reports` (JUnit Testinfra + логи контейнера)

## Експерименти
- [#2](https://github.com/wlysenko/devops-pr6/actions/runs/44609426949) — зламаний тест: `test` впав, `build` і `deploy` пропущені
- [#3](https://github.com/wlysenko/devops-pr6/actions/runs/44609560240) — несправний `/health`: деплой впав, автоматичний відкат на `stable`, запуск = failure
