#!/bin/bash

set -e

############################
# モデルの保存
############################ 
docker exec -it save_tf_model python3 /app/scripts/main.py -e 20 -c ./models/checkpoints -s ./models/saved_model -f ./models/model.h5
