#!/bin/bash
git clone https://github.com/salvatore-abello/quakewatch/
docker compose -f ./quakewatch/prod/docker-compose.yml up --build
