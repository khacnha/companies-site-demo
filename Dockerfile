FROM python:3.11
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY .env /app/.env
RUN pip install -r requirements.txt
COPY . /app

