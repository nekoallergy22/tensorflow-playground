#!/bin/bash

docker rm -f save_tf_model
docker rmi save_tf_model

docker ps -a
docker images
