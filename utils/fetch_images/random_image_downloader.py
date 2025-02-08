#!/usr/bin/env python3

import argparse
import requests
from pathlib import Path


class RandomImageDownloader:
    def __init__(self, save_dir: str) -> None:
        self.save_dir = Path(save_dir)
        self._create_save_dir()
    
    def _create_save_dir(self) -> None:
        if not self.save_dir.exists():
            self.save_dir.mkdir(parents=True)

    def download_images(self, count: int, width: int = 800, height: int = 600) -> None:
        for i in range(1, count + 1):
            url = f"https://picsum.photos/{width}/{height}?random={i}"
            self._download_image(url, i)

    def _download_image(self, url: str, index: int) -> None:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            file_path = self.save_dir / f"image_{index}.jpg"
            with open(file_path, "wb") as f:
                f.write(response.content)
            
            print(f"画像 {index} をダウンロードしました")
            
        except requests.RequestException as e:
            print(f"画像 {index} のダウンロードに失敗しました: {e}")


def parse_args():
    parser = argparse.ArgumentParser(description="Picsumからランダムな画像をダウンロード")
    parser.add_argument("-d", "--directory", default="images", help="画像を保存するディレクトリ (デフォルト: images)")
    parser.add_argument("-n", "--number", type=int, default=1, help="ダウンロードする画像の枚数 (デフォルト: 1)")
    parser.add_argument("--width", type=int, default=800, help="画像の幅 (デフォルト: 800)")
    parser.add_argument("--height", type=int, default=600, help="画像の高さ (デフォルト: 600)")
    return parser.parse_args()


def main():
    args = parse_args()
    downloader = RandomImageDownloader(args.directory)
    downloader.download_images(args.number, args.width, args.height)


if __name__ == "__main__":
    main()
