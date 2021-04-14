FROM python:3.8-alpine
WORKDIR /code
RUN pip install fastapi
RUN pip install uvicorn[standar]
COPY ./src/api/main.py ./code
EXPOSE 8889