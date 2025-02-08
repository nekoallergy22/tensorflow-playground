import argparse
from pathlib import Path
import sys
import tensorflow as tf
from tensorflow.keras.datasets import mnist

from base_handler import DataHandler
from config import TRAIN_FILENAME, TEST_FILENAME
from logger import setup_logger
from config import LOG_DIR

logger = setup_logger(LOG_DIR)

class MnistHandler(DataHandler):
    def save_mnist_as_tfrecord(self) -> None:
        logger.info('MNISTデータをTFRecordとして保存します')
        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        self._save_dataset(x_train, y_train, TRAIN_FILENAME, 'train')
        self._save_dataset(x_test, y_test, TEST_FILENAME, 'test')
        
        logger.info('MNISTデータのTFRecord保存が完了しました')

def main():
    try:
        logger.info("プログラムを開始します")
        
        parser = argparse.ArgumentParser(description='MNISTデータをTFRecordとして保存/読み込み')
        parser.add_argument('--data_dir', type=Path, default='data', help='データディレクトリ')
        parser.add_argument('--operation', type=str, choices=['save', 'load'], required=True)
        args = parser.parse_args()

        handler = MnistHandler(args.data_dir)
        if args.operation == 'save':
            handler.save_mnist_as_tfrecord()
        else:
            handler.load_tfrecord_and_display(TRAIN_FILENAME)
            handler.load_tfrecord_and_display(TEST_FILENAME)

        logger.info("プログラムが正常に終了しました")
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
