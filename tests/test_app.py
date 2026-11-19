import pytest

from app.config import ConfigError, load_config
from app.main import create_app


@pytest.mark.parametrize("url", ["/health", "/version"])
def test_endpoints_return_200(client, url):
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.is_json


def test_health_status_ok(client):
    data = client.get("/health").get_json()
    assert data["status"] == "OK"  # ЕКСПЕРИМЕНТ 1: навмисно зламаний тест
    assert data["uptime_sec"] >= 0


def test_version_default(monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    c = create_app().test_client()
    assert c.get("/version").get_json()["version"] == "1.0.0"


@pytest.mark.parametrize("ver", ["1.0.0", "1.1.0", "2.0.0-rc1"])
def test_version_from_env(monkeypatch, ver):
    monkeypatch.setenv("APP_VERSION", ver)
    c = create_app().test_client()
    assert c.get("/version").get_json()["version"] == ver


def test_unknown_url_404(client):
    assert client.get("/nope").status_code == 404


# поведінка за неправильних налаштувань
@pytest.mark.parametrize(
    "var, value",
    [
        ("APP_VERSION", "latest"),
        ("APP_VERSION", "1.0"),
        ("APP_ENV", "production"),
        ("PORT", "abc"),
        ("PORT", "70000"),
    ],
)
def test_bad_config_rejected(monkeypatch, var, value):
    monkeypatch.setenv(var, value)
    with pytest.raises(ConfigError):
        load_config()
    with pytest.raises(ConfigError):
        create_app()


def test_good_config_parsed(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "1.2.3")
    monkeypatch.setenv("APP_ENV", "prod")
    monkeypatch.setenv("PORT", "8080")
    assert load_config() == {"version": "1.2.3", "env": "prod", "port": 8080}
