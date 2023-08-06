#!/bin/bash
docker ps -aq | xargs docker stop | xargs docker rm
docker volume rm $(docker volume ls -qf dangling=true)

docker-compose -f docker-compose.postgres.yml up --build -d
docker-compose -f docker-compose.milvus.yml up --build -d
docker-compose -f docker-compose.app.yml up --build -d
docker-compose -f docker-compose.appsmith.yml up --build -d