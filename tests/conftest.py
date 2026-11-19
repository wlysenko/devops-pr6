import pytest

from app.main import create_app


@pytest.fixture
def client(monkeypatch):
    # чисте оточення для кожного тесту
    for var in ("APP_VERSION", "APP_ENV", "PORT"):
        monkeypatch.delenv(var, raising=False)
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c
