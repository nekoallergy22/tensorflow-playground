#!/bin/bash

set -e

############################
# # MNIST
############################
# データの保存
docker exec -it sample_tfrecord python3 /app/scripts/mnist_handler.py \
    --data_dir /app/data \
    --operation save

# データの読み込み
docker exec -it sample_tfrecord python3 /app/scripts/mnist_handler.py \
    --data_dir /app/data \
    --operation load


############################
# 一般画像
############################
# データの保存
docker exec -it sample_tfrecord python3 /app/scripts/image_handler.py \
    --data_dir /app/data \
    --image_dir /app/images \
    --operation save \
    --output_filename images.tfrecord

# データの読み込み
docker exec -it sample_tfrecord python3 /app/scripts/image_handler.py \
    --data_dir /app/data \
    --operation load \
    --output_filename images.tfrecord
