# MNIST TFRecord Converter

MNIST データセットを TFRecord 形式に変換し、保存・読み込みを行うツール

## 概要

このツールは以下の機能を提供します：

- MNIST データセットの TFRecord 形式への変換
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

### データの保存

MNIST データセットを TFRecord 形式に変換して保存します：

```
docker exec -it mnist_tfrecord python3 /app/scripts/main.py --data_dir /app/data --operation save
```

保存されるファイル：

- `data/mnist_train.tfrecord`: 訓練データ
- `data/mnist_test.tfrecord`: テストデータ

### データの読み込み

保存した TFRecord ファイルを読み込み、データの統計情報を表示します：

```
docker exec -it mnist_tfrecord python3 /app/scripts/main.py --data_dir /app/data --operation load
```

### オプション

- `--data_dir`: データの保存・読み込み先ディレクトリ（デフォルト: `data`）
- `--operation`: 実行する操作（`save`または`load`）

## プロジェクト構造

```
.
├── Dockerfile
├── README.md
├── compose.yml
├── data/ # データ保存ディレクトリ
├── launch.sh # 環境構築スクリプト
├── logs/ # ログ保存ディレクトリ
├── requirements.txt
└── scripts/
├── config.py # 設定ファイル読み込み
├── config.yml # 設定値
├── logger.py # ロギング設定
├── main.py # メインスクリプト
└── run.sh # 実行スクリプト
```

## ログ

実行ログは`logs`ディレクトリに保存されます。ログファイル名は実行時のタイムスタンプに基づいて生成されます。

## 設定

`scripts/config.yml`で以下の設定が可能です：

- `DATA_DIR`: データ保存ディレクトリ
- `LOG_DIR`: ログ保存ディレクトリ
- `TRAIN_FILENAME`: 訓練データのファイル名
- `TEST_FILENAME`: テストデータのファイル名
