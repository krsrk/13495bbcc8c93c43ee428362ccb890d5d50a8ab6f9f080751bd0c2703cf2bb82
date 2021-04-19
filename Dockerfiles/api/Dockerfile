FROM python:3.8-alpine
WORKDIR /code
RUN pip install fastapi
RUN pip install uvicorn[standar]
RUN pip install peewee

#mysqlclient installation
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev
RUN pip install mysqlclient
RUN apk del build-deps

COPY ./src/api/main.py ./code
EXPOSE 8889