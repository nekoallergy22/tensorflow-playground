# TFRecord Converter for MNIST and Custom Images

TFRecord 形式に変換し、保存・読み込みを行うツール

## 概要

このツールは以下の機能を提供します：

- MNIST データセットの TFRecord 形式への変換
- 一般画像の TFRecord 形式への変換
- 変換したデータの読み込みと統計情報の表示

## 必要条件

- Docker
- Docker Compose

## セットアップ

1. リポジトリのクローン

```

git clone https://github.com/nekoallergy22/tensorflow-playground.git
cd tensorflow-playground/basic/tfrecord

```

2. 環境構築

```

./launch.sh

```

## 使用方法

### MNIST データの変換

#### データの保存

```
docker exec -it mnist_tfrecord python3 /app/scripts/mnist_handler.py \
 --data_dir /app/data \
 --operation save
```

保存されるファイル：

- `data/mnist_train.tfrecord`: 訓練データ
- `data/mnist_test.tfrecord`: テストデータ

#### データの読み込み

```
docker exec -it mnist_tfrecord python3 /app/scripts/mnist_handler.py \
 --data_dir /app/data \
 --operation load
```

### 一般画像の変換

#### 画像データの準備

画像データは以下のディレクトリ構造で準備してください：

```
images/
├── 0/ # ラベル名（数字）のディレクトリ
│ ├── image1.jpg
│ ├── image2.jpg
│ └── ...
├── 1/
│ ├── image1.jpg
│ ├── image2.jpg
│ └── ...
└── ...
```

- ディレクトリ名が画像のラベルとして使用されます
- サポートする拡張子: .jpg, .jpeg, .png
- 画像は自動的に 28x28 のグレースケールに変換されます

#### データの保存

```
docker exec -it mnist_tfrecord python3 /app/scripts/image_handler.py \
 --data_dir /app/data \
 --image_dir /app/images \
 --operation save \
 --output_filename images.tfrecord
```

#### データの読み込み

```
docker exec -it mnist_tfrecord python3 /app/scripts/image_handler.py \
 --data_dir /app/data \
 --operation load \
 --output_filename images.tfrecord
```

### オプション

共通オプション：

- `--data_dir`: データの保存・読み込み先ディレクトリ（デフォルト: `data`）
- `--operation`: 実行する操作（`save`または`load`）

image_handler.py 固有のオプション：

- `--image_dir`: 変換する画像が格納されているディレクトリ
- `--output_filename`: 出力する TFRecord ファイル名

## プロジェクト構造

```
.
├── Dockerfile
├── README.md
├── compose.yml
├── data/ # データ保存ディレクトリ
├── images/ # 画像データディレクトリ
├── launch.sh # 環境構築スクリプト
├── logs/ # ログ保存ディレクトリ
├── requirements.txt
└── scripts/
    ├── base_handler.py # 基底クラス
    ├── mnist_handler.py # MNIST 用ハンドラ
    ├── image_handler.py # 一般画像用ハンドラ
    ├── config.py # 設定ファイル読み込み
    ├── config.yml # 設定値
    └── logger.py # ロギング設定
```

## ログ

実行ログは`logs`ディレクトリに保存されます。ログファイル名は実行時のタイムスタンプに基づいて生成されます。

## 設定

`scripts/config.yml`で以下の設定が可能です：

- `DATA_DIR`: データ保存ディレクトリ
- `LOG_DIR`: ログ保存ディレクトリ
- `TRAIN_FILENAME`: MNIST の訓練データファイル名
- `TEST_FILENAME`: MNIST のテストデータファイル名
