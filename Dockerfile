FROM python:3.9-alpine3.13

LABEL maintainer="django_docker_starter.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./backend /backend
COPY ./scripts /scripts

WORKDIR /backend

EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home appuser && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R appuser:appuser /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER appuser

CMD ["run.sh"]