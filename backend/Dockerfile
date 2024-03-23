FROM python:latest

RUN mkdir /app
ADD requirements.txt /app
WORKDIR /app

RUN pip install -r requirements.txt 

RUN groupadd appgroup && useradd -g appgroup appuser
RUN apt-get update \
    && apt-get upgrade -y\
    && apt install -y supervisor default-mysql-client

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 10101

COPY config/supervisord.conf /etc/supervisord.conf

COPY app .
WORKDIR /

ENTRYPOINT [ "/usr/bin/supervisord", "-c", "/etc/supervisord.conf" ]