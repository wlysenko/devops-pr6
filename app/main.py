import os
from datetime import datetime, timezone

from flask import Flask, jsonify

DEFAULT_VERSION = "1.0.0"


def get_version():
    # версію беремо з оточення, щоб її можна було змінити без перезбірки коду
    return os.getenv("APP_VERSION", DEFAULT_VERSION)


def create_app():
    app = Flask(__name__)
    started = datetime.now(timezone.utc)

    @app.get("/health")
    def health():
        uptime = (datetime.now(timezone.utc) - started).total_seconds()
        return jsonify(status="ok", uptime_sec=round(uptime, 1))

    @app.get("/version")
    def version():
        return jsonify(
            version=get_version(),
            env=os.getenv("APP_ENV", "dev"),
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
