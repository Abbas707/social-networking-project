FROM python:3.11.1-slim

# environments
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/social_networking_project/

WORKDIR social_networking_project

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y libmagic-dev

# copy code base
COPY . .
