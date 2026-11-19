from datetime import datetime, timezone

from flask import Flask, jsonify

from app.config import load_config


def create_app():
    cfg = load_config()  # з неправильними змінними застосунок не створиться
    app = Flask(__name__)
    started = datetime.now(timezone.utc)

    @app.get("/health")
    def health():
        uptime = (datetime.now(timezone.utc) - started).total_seconds()
        return jsonify(status="ok", uptime_sec=round(uptime, 1))

    @app.get("/version")
    def version():
        return jsonify(version=cfg["version"], env=cfg["env"])

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=load_config()["port"])
