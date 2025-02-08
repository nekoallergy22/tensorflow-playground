#!/bin/bash

set -e

# データの保存
docker exec -it mnist_tfrecord python3 /app/scripts/main.py --data_dir /app/data --operation save

# データの読み込み
docker exec -it mnist_tfrecord python3 /app/scripts/main.py --data_dir /app/data --operation load

