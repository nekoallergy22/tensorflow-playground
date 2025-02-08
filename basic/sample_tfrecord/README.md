# TFRecord Converter for MNIST and Custom Images

A tool for converting MNIST dataset and custom images to TFRecord format, with save and load functionality

## Overview

This tool provides the following features:

- Convert MNIST dataset to TFRecord format
- Convert custom images to TFRecord format
- Load converted data and display statistics

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository

```bash
git clone https://github.com/nekoallergy22/tensorflow-playground.git
cd tensorflow-playground/basic/tfrecord
```

2. Build environment

```bash
./launch.sh
```

## Usage

### MNIST Data Conversion

#### Save Data

```bash
docker exec -it mnist_tfrecord python3 /app/scripts/mnist_handler.py \
 --data_dir /app/data \
 --operation save
```

Generated files:

- `data/mnist_train.tfrecord`: Training data
- `data/mnist_test.tfrecord`: Test data

#### Load Data

```bash
docker exec -it mnist_tfrecord python3 /app/scripts/mnist_handler.py \
 --data_dir /app/data \
 --operation load
```

### Custom Image Conversion

#### Prepare Image Data

Organize your images in the following directory structure:

```
images/
├── 0/  # Directory name is used as label
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── 1/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── ...
```

- Directory names are used as image labels
- Supported extensions: .jpg, .jpeg, .png
- Images are automatically converted to 28x28 grayscale

#### Save Data

```bash
docker exec -it mnist_tfrecord python3 /app/scripts/image_handler.py \
 --data_dir /app/data \
 --image_dir /app/images \
 --operation save \
 --output_filename images.tfrecord
```

#### Load Data

```bash
docker exec -it mnist_tfrecord python3 /app/scripts/image_handler.py \
 --data_dir /app/data \
 --operation load \
 --output_filename images.tfrecord
```

### Options

Common options:

- `--data_dir`: Directory for saving/loading data (default: `data`)
- `--operation`: Operation to execute (`save` or `load`)

image_handler.py specific options:

- `--image_dir`: Directory containing images to convert
- `--output_filename`: Output TFRecord filename

## Project Structure

```
.
├── Dockerfile
├── README.md
├── compose.yml
├── data/              # Data storage directory
├── images/            # Image data directory
├── launch.sh          # Environment setup script
├── logs/              # Log storage directory
├── requirements.txt
└── scripts/
    ├── base_handler.py    # Base class
    ├── mnist_handler.py   # MNIST handler
    ├── image_handler.py   # Custom image handler
    ├── config.py         # Configuration loader
    ├── config.yml        # Configuration values
    └── logger.py         # Logging setup
```

## Logging

Execution logs are stored in the `logs` directory. Log filenames are generated based on execution timestamps.

## Configuration

The following settings can be configured in `scripts/config.yml`:

- `DATA_DIR`: Data storage directory
- `LOG_DIR`: Log storage directory
- `TRAIN_FILENAME`: MNIST training data filename
- `TEST_FILENAME`: MNIST test data filename
