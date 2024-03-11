from python:3.12-alpine

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r /requirements.txt && pip install gunicorn
COPY ./src /app

RUN mkdir /data/
ENV DB_DRIVER=sqlite \
    DB_USER='' \
    DB_PASSWORD='' \
    DB_HOST='//data/db.sqlite' \
    DB_PORT='' \
    DB_SCHEMA=''

WORKDIR /app
CMD ["/usr/local/bin/gunicorn", "-c", "/app/gunicorn.conf.py", "app:app"]
