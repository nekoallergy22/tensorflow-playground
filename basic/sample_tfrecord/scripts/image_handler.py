import argparse
from pathlib import Path
import sys
import numpy as np
from PIL import Image

from base_handler import DataHandler
from logger import setup_logger
from config import LOG_DIR

logger = setup_logger(LOG_DIR)


class ImageHandler(DataHandler):
    def save_images_as_tfrecord(self, image_dir: Path, output_filename: str) -> None:
        logger.info(f'{image_dir}の画像をTFRecordとして保存します')
        
        images = []
        labels = []
        valid_extensions = {'.jpg', '.jpeg', '.png'}
        
        # ラベルごとのディレクトリを処理
        for label_dir in image_dir.iterdir():
            if not label_dir.is_dir():
                continue
                
            try:
                label = int(label_dir.name)
            except ValueError:
                logger.warning(f'ディレクトリ名を数値に変換できません: {label_dir.name}')
                continue
            
            # 各ディレクトリ内の画像を処理
            for img_path in label_dir.iterdir():
                if img_path.suffix.lower() not in valid_extensions:
                    continue
                    
                try:
                    img = Image.open(img_path).convert('L')  # グレースケール変換
                    img = img.resize((28, 28))  # MNISTと同じサイズに
                    img_array = np.array(img)
                    
                    images.append(img_array)
                    labels.append(label)
                    logger.info(f'画像を読み込みました: {img_path}, ラベル: {label}')
                except Exception as e:
                    logger.warning(f'画像の読み込みに失敗しました: {img_path}, エラー: {e}')
                    continue

        if not images:
            logger.error('有効な画像が見つかりませんでした')
            return

        self._save_dataset(images, labels, output_filename, 'image')
        logger.info(f'画像データのTFRecord保存が完了しました（合計: {len(images)}件）')


def main():
    try:
        logger.info("プログラムを開始します")
        
        parser = argparse.ArgumentParser(description='画像データをTFRecordとして保存/読み込み')
        parser.add_argument('--data_dir', type=Path, default='data', help='出力ディレクトリ')
        parser.add_argument('--operation', type=str, choices=['save', 'load'], required=True)
        parser.add_argument('--output_filename', type=str, default='images.tfrecord')
        
        # save操作の場合のみ必要な引数
        if '--operation' not in sys.argv or 'save' in sys.argv:
            parser.add_argument('--image_dir', type=Path, required=True, help='画像ディレクトリ')
        
        args = parser.parse_args()

        handler = ImageHandler(args.data_dir)
        if args.operation == 'save':
            handler.save_images_as_tfrecord(args.image_dir, args.output_filename)
        else:
            handler.load_tfrecord_and_display(args.output_filename)

        logger.info("プログラムが正常に終了しました")
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
