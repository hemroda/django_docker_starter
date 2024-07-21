FROM python:3.12.4-alpine3.20

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk add --upgrade --no-cache build-base linux-headers && \
    pip install --upgrade pip && \
    pip install -r /requirements.txt

COPY app/ /app

WORKDIR /app

RUN adduser --disabled-password --no-create-home appuser

USER appuser

CMD ["uwsgi", "--socket", ":9000", "--workers", "4", "--master", "--enabled-threads", "--module", "app.wsgi"]
