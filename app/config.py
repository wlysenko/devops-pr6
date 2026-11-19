import os
import re

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(-[0-9A-Za-z.]+)?$")
ALLOWED_ENVS = {"dev", "test", "prod"}


class ConfigError(ValueError):
    pass


def load_config():
    """Читає налаштування зі змінних середовища і перевіряє їх.
    Неправильне значення -> ConfigError, сервіс не стартує з поганим конфігом."""
    version = os.getenv("APP_VERSION", "1.0.0")
    env = os.getenv("APP_ENV", "dev")
    port_raw = os.getenv("PORT", "8000")

    if not VERSION_RE.match(version):
        raise ConfigError(f"APP_VERSION має бути у форматі X.Y.Z, отримано: {version!r}")
    if env not in ALLOWED_ENVS:
        raise ConfigError(f"APP_ENV має бути одним з {sorted(ALLOWED_ENVS)}, отримано: {env!r}")
    try:
        port = int(port_raw)
    except ValueError:
        raise ConfigError(f"PORT має бути числом, отримано: {port_raw!r}") from None
    if not 1 <= port <= 65535:
        raise ConfigError(f"PORT поза діапазоном 1-65535: {port}")

    return {"version": version, "env": env, "port": port}
