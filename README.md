# ПР6 — Python-сервіс у Docker + pytest + Testinfra + CI + відкат

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/pytest tests/test_app.py                       # модульні тести
./scripts/deploy.sh 1.0.0                                # збірка і запуск
APP_VERSION=1.0.0 .venv/bin/pytest tests/test_infra.py --hosts=docker://pr6-service
./scripts/deploy.sh 1.1.0                                # оновлення
./scripts/rollback.sh                                    # відкат на попередню
docker compose down
```
