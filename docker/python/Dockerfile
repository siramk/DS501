FROM python:3.7.3-stretch

RUN apt-get -y update && apt-get install -y apt-transport-https

RUN apt-get update && apt-get install -y netcat

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

COPY scripts/bashrc /root/.bashrc

WORKDIR /work