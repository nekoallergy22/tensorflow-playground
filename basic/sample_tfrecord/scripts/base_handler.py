from pathlib import Path
from typing import Dict, Any, List
import tensorflow as tf
import numpy as np
from logger import setup_logger
from config import LOG_DIR

logger = setup_logger(LOG_DIR)

class DataHandler:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _create_example(self, img: np.ndarray, label: Any) -> tf.train.Example:
        img_bytes = img.tobytes()
        feature = {
            'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_bytes])),
            'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label]))
        }
        return tf.train.Example(features=tf.train.Features(feature=feature))

    def _save_dataset(self, images: List[np.ndarray], labels: List[Any], 
                     filename: str, dataset_type: str) -> None:
        filepath = self.data_dir / filename
        total = len(images)
        
        logger.info(f'{dataset_type}データセットの保存を開始します（{total}件）')
        with tf.io.TFRecordWriter(str(filepath)) as writer:
            for i, (img, label) in enumerate(zip(images, labels), 1):
                example = self._create_example(img, label)
                writer.write(example.SerializeToString())
                if i % 100 == 0:
                    logger.info(f'進捗: {i}/{total}件完了')

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
