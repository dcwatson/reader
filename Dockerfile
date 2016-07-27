FROM python:3.5-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /reader
ADD . /reader/

RUN set -ex \
    && apk add --no-cache postgresql-dev uwsgi \
    && apk add --no-cache --virtual .build-deps musl-dev gcc \
    && pip install --no-cache-dir -r /reader/requirements.txt \
    && apk del .build-deps \
    && rm -rf ~/.cache

EXPOSE 8000

ENTRYPOINT ["python", "/reader/manage.py"]
CMD ["shell"]
