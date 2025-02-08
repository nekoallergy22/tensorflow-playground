#!/bin/bash

docker rm -f mnist_tfrecord
docker rmi mnist_tfrecord


docker ps -a
docker images
