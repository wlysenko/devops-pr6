FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# procps та iproute2 потрібні для перевірок Testinfra (ps, ss)
RUN apt-get update && apt-get install -y --no-install-recommends procps iproute2 \
    && rm -rf /var/lib/apt/lists/*

# окремий користувач без прав root
RUN groupadd --system app && useradd --system --gid app --no-create-home app

WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app

USER app
EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:' + __import__('os').getenv('PORT','8000') + '/health', timeout=2)" || exit 1

CMD exec gunicorn -b 0.0.0.0:8001 -w 2 --timeout 30 "app.main:create_app()"
