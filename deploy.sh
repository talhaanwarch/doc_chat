#!/bin/bash

docker compose -f docker-compose.milvus.yml up --build -d
docker compose -f docker-compose.app.yml up --build -d
docker compose -f docker-compose.tooljet.yml up --build -d