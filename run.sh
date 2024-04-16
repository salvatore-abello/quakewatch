#!/bin/bash
git clone https://github.com/salvatore-abello/quakewatch/
cd ./quakewatch/prod
echo "Changed directory to: $(pwd)"
docker compose  up --build
