import pytest


@pytest.mark.parametrize("url", ["/health", "/version"])
def test_endpoints_return_200(client, url):
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.is_json


def test_health_status_ok(client):
    data = client.get("/health").get_json()
    assert data["status"] == "ok"
    assert data["uptime_sec"] >= 0


def test_version_default(client, monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    assert client.get("/version").get_json()["version"] == "1.0.0"


@pytest.mark.parametrize("ver", ["1.0.0", "1.1.0", "2.0.0-rc1"])
def test_version_from_env(client, monkeypatch, ver):
    monkeypatch.setenv("APP_VERSION", ver)
    assert client.get("/version").get_json()["version"] == ver


def test_unknown_url_404(client):
    assert client.get("/nope").status_code == 404
