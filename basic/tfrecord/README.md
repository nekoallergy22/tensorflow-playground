# MNIST TFRecord Converter

A tool for converting MNIST dataset to TFRecord format, with save and load functionality

## Overview

This tool provides the following features:

- Convert MNIST dataset to TFRecord format
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

### Saving Data

Convert MNIST dataset to TFRecord format:

```bash
docker exec -it mnist_tfrecord python3 /app/scripts/main.py --data_dir /app/data --operation save
```

Generated files:

- `data/mnist_train.tfrecord`: Training data
- `data/mnist_test.tfrecord`: Test data

### Loading Data

Load saved TFRecord files and display data statistics:

```bash
docker exec -it mnist_tfrecord python3 /app/scripts/main.py --data_dir /app/data --operation load
```

### Options

- `--data_dir`: Directory for saving/loading data (default: `data`)
- `--operation`: Operation to execute (`save` or `load`)

## Project Structure

```bash
.
├── Dockerfile
├── README.md
├── compose.yml
├── data/          # Data storage directory
├── launch.sh      # Environment setup script
├── logs/          # Log storage directory
├── requirements.txt
└── scripts/
    ├── config.py  # Configuration loader
    ├── config.yml # Configuration values
    ├── logger.py  # Logging setup
    ├── main.py    # Main script
    └── run.sh     # Execution script
```

## Logging

Execution logs are stored in the `logs` directory. Log filenames are generated based on execution timestamps.

## Configuration

The following settings can be configured in `scripts/config.yml`:

- `DATA_DIR`: Data storage directory
- `LOG_DIR`: Log storage directory
- `TRAIN_FILENAME`: Training data filename
- `TEST_FILENAME`: Test data filename
