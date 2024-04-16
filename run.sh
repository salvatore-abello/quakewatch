#!/bin/bash
git clone https://github.com/salvatore-abello/quakewatch/docker-compose.yml
docker compose -f ./quakewatch up --build
