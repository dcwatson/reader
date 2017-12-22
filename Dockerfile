FROM python:3-slim

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /reader/
RUN pip install -Ur /reader/requirements.txt

COPY . /reader

RUN python /reader/manage.py collectstatic --noinput && \
    useradd -g root -MN reader && \
    chown -R reader:0 /reader && \
    chmod g+s /reader

WORKDIR /reader
USER reader

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--access-logfile", "-", "reader.wsgi"]
