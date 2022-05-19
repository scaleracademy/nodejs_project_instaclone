# syntax=docker/dockerfile:1
FROM python:3.9.6-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/instaclone

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev build-base py-pip jpeg-dev zlib-dev

ENV LIBRARY_PATH=/lib:/usr/lib

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver"]

