FROM python:3.6

ENV PYTHONUNBUFFERED 1

COPY . /code/
WORKDIR /code/

RUN apt-get -y update
RUN pip install pipenv
RUN pipenv install --system && pipenv install --dev --system

EXPOSE 8000