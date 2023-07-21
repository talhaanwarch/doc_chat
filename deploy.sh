#!/bin/bash

# Run the original commands
docker-compose -f docker-compose.milvus.yml up --build -d
docker-compose -f docker-compose.app.yml up --build -d
docker-compose -f docker-compose.tooljet.yml up --build -d
docker-compose -f docker-compose.npm.yml up --build -d

# Check for errors
if [ $? -ne 0 ]; then
    # Run the alternative commands
    docker compose -f docker-compose.milvus.yml up --build -d
    docker compose -f docker-compose.app.yml up --build -d
    docker compose -f docker-compose.tooljet.yml up --build -d
fi
