FROM python:3.7-alpine

COPY . /app
WORKDIR /app

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libressl-dev libffi-dev\
     && pip install -r requirements.txt \
     && apk del .build-deps gcc musl-dev libressl-dev libffi-dev

ENTRYPOINT ["python3", "scrap.py"]
