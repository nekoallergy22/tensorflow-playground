#!/bin/bash

docker compose -f compose.yml stop
docker compose -f compose.yml up -d 
