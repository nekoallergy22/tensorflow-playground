import argparse
import sys
from pathlib import Path
from typing import Dict

import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import mnist

from config import DATA_DIR, LOG_DIR, TRAIN_FILENAME, TEST_FILENAME
from logger import setup_logger

logger = setup_logger(LOG_DIR)


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='MNISTデータをTFRecordとして保存/読み込みするスクリプト')
        self._add_arguments()

    def _add_arguments(self) -> None:
        self.parser.add_argument('--data_dir', type=Path, default=DATA_DIR, help='データディレクトリのパス')
        self.parser.add_argument('--operation', type=str, choices=['save', 'load'], required=True, help='実行する操作（saveまたはload）')

    def parse(self):
        return self.parser.parse_args()
    

class MnistDataHandler:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save_mnist_as_tfrecord(self) -> None:
        logger.info('MNISTデータをTFRecordとして保存します')
        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        self._save_dataset(x_train, y_train, TRAIN_FILENAME, 'train')
        self._save_dataset(x_test, y_test, TEST_FILENAME, 'test')
        
        logger.info('MNISTデータのTFRecord保存が完了しました')

    def _save_dataset(self, images: np.ndarray, labels: np.ndarray, 
                     filename: str, dataset_type: str) -> None:
        filepath = self.data_dir / filename
        total = len(images)
        
        logger.info(f'{dataset_type}データセットの保存を開始します（{total}件）')
        with tf.io.TFRecordWriter(str(filepath)) as writer:
            for i, (img, label) in enumerate(zip(images, labels), 1):
                example = self._create_example(img, label)
                writer.write(example.SerializeToString())
                if i % 10000 == 0:
                    logger.info(f'進捗: {i}/{total}件完了')

    def _create_example(self, img: np.ndarray, label: int) -> tf.train.Example:
        feature = {
            'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img.tobytes()])),
            'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label]))
        }
        return tf.train.Example(features=tf.train.Features(feature=feature))

    def load_tfrecord_and_display(self, filename: str) -> None:
        filepath = self.data_dir / filename
        if not filepath.exists():
            logger.error(f"ファイルが存在しません: {filepath}")
            return
            
        logger.info(f'{filepath}を読み込んで情報を表示します')
        try:
            dataset = tf.data.TFRecordDataset(str(filepath))
            label_count = self._count_labels(dataset)
            
            logger.info(f'データ数: {sum(label_count.values())}')
            logger.info(f'ラベルの分布: {dict(sorted(label_count.items()))}')
        except Exception as e:
            logger.error(f"データの読み込み中にエラーが発生しました: {e}")

    def _count_labels(self, dataset: tf.data.TFRecordDataset) -> Dict[int, int]:
        label_count: Dict[int, int] = {}
        for serialized_example in dataset:
            example = tf.train.Example.FromString(serialized_example.numpy())
            label = example.features.feature['label'].int64_list.value[0]
            label_count[label] = label_count.get(label, 0) + 1
        return label_count

def main() -> None:

    logger.info("プログラムを開始します")
    
    args = ArgumentParser().parse()
    data_handler = MnistDataHandler(args.data_dir)
    
    if args.operation == 'save':
        data_handler.save_mnist_as_tfrecord()
    else: 
        data_handler.load_tfrecord_and_display(TRAIN_FILENAME)
        data_handler.load_tfrecord_and_display(TEST_FILENAME)
    
    logger.info("プログラムが正常に終了しました")


if __name__ == '__main__':
    main()