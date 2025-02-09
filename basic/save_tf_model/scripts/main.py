import argparse
import logging
import os
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

from config import LOG_DIR
from logger import setup_logger


logger = setup_logger(LOG_DIR)

class ModelSaver:
    def __init__(self, args):
        self.args = args
        self.model = None

    def create_model(self):
        model = models.Sequential([
            layers.Dense(64, activation='relu', input_shape=(10,)),
            layers.Dense(32, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        return model

    def setup_checkpoints(self):
        checkpoint_path = os.path.join(self.args.checkpoint_dir, 'cp-{epoch:04d}.ckpt')
        return tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_path,
            save_weights_only=True,
            verbose=1,
            period=1
        )

    def generate_sample_data(self):
        x_train = np.random.random((1000, 10))
        y_train = np.random.randint(2, size=(1000, 1))
        return x_train, y_train

    def train_and_save(self):
        self.model = self.create_model()
        x_train, y_train = self.generate_sample_data()
        
        # チェックポイントディレクトリの作成
        Path(self.args.checkpoint_dir).mkdir(parents=True, exist_ok=True)
        
        # トレーニングの実行
        logger.info("トレーニングを開始します")
        self.model.fit(
            x_train, y_train,
            epochs=self.args.epochs,
            callbacks=[self.setup_checkpoints()]
        )

        # SavedModel形式で保存
        logger.info(f"SavedModel形式で保存: {self.args.saved_model_dir}")
        self.model.save(self.args.saved_model_dir, save_format='tf')

        # HDF5形式で保存
        logger.info(f"HDF5形式で保存: {self.args.h5_file}")
        self.model.save(self.args.h5_file, save_format='h5')


def get_parser():
    parser = argparse.ArgumentParser(description='モデルの学習と保存を行います')
    parser.add_argument('-e', '--epochs', type=int, default=10, help='学習エポック数')
    parser.add_argument('-c', '--checkpoint_dir', type=str, default='checkpoints', help='チェックポイント保存ディレクトリ')
    parser.add_argument('-s', '--saved_model_dir', type=str, default='saved_model', help='SavedModel保存ディレクトリ')
    parser.add_argument('-f', '--h5_file', type=str, default='model.h5', help='HDF5ファイルの保存パス')
    return parser.parser.parse_args()


def main():  
    logger.info("プログラムを開始します")
    
    # 引数の解析
    args = get_parser()
    
    # モデルの学習と保存
    model_saver = ModelSaver(args)
    model_saver.train_and_save()
    
    logger.info("プログラムが正常に終了しました")


if __name__ == '__main__':
    main()
