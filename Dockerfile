FROM python:3.12.4-alpine3.20

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /requirements.txt

RUN apk add --upgrade --no-cache build-base linux-headers python3-dev && \
    pip install --upgrade pip && \
    python -m venv /venv && \
    /venv/bin/pip install -r /requirements.txt && \
    apk del build-base linux-headers python3-dev

COPY app/ /app

WORKDIR /app

RUN adduser --disabled-password --no-create-home appuser && \
    chown -R appuser:appuser /app /venv

USER appuser

ENV PATH="/venv/bin:$PATH"

CMD ["/venv/bin/uwsgi", "--socket", ":9000", "--workers", "4", "--master", "--enable-threads", "--module", "app.wsgi"]
