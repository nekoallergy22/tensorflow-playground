#!/bin/bash

docker rm -f sample_tfrecord
docker rmi sample_tfrecord

docker ps -a
docker images
