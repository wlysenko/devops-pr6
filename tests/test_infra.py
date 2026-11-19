"""Testinfra-перевірки запущеного контейнера.
Запуск: pytest tests/test_infra.py --hosts=docker://pr6-service
"""
import os

import pytest

pytestmark = pytest.mark.infra


def test_runs_as_non_root(host):
    assert host.user().name == "app"
    assert host.user().uid != 0


def test_gunicorn_running(host):
    procs = host.process.filter(comm="gunicorn")
    assert len(procs) >= 1
    for p in procs:
        assert p.user == "app"


def test_listens_on_8000(host):
    assert host.socket("tcp://0.0.0.0:8000").is_listening


def test_app_files_present(host):
    f = host.file("/srv/app/main.py")
    assert f.exists
    assert f.user == "root"  # код належить root, процес його лише читає


def test_root_fs_read_only(host):
    # /etc належить root, але навіть так помилка має бути саме read-only
    cmd = host.run("touch /etc/pr6_test")
    assert cmd.rc != 0
    assert "Read-only file system" in cmd.stderr
    # а в tmpfs /tmp писати можна
    assert host.run("touch /tmp/ok").rc == 0


def test_health_inside_container(host):
    cmd = host.run(
        "python -c \"import urllib.request;print(urllib.request.urlopen('http://127.0.0.1:8000/health').read().decode())\""
    )
    assert cmd.rc == 0
    assert '"status":"ok"' in cmd.stdout.replace(" ", "")


def test_version_matches_env(host):
    expected = os.getenv("APP_VERSION", "1.0.0")
    assert host.environment()["APP_VERSION"] == expected
