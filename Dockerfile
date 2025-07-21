# docker build -t blk-hacking-mx-Leonardo-Lameda .
From ubuntu:latest

FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-venv

COPY . ./app 

WORKDIR /app

RUN python3 -m venv .venv && . .venv/bin/activate  && pip3 install -r requirements.txt


