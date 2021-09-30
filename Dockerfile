FROM python:3.6-buster

RUN pip install --upgrade pip
RUN apt-get -y update && apt-get -y upgrade

COPY . /app
WORKDIR /app

RUN pip install -r requirements/prod.txt

EXPOSE 5000

ENTRYPOINT [ "scripts/run.sh"]
