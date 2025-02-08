import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

def setup_logger(log_dir: Path, file_name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger('mnist_tfrecord')
    
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_dir.mkdir(parents=True, exist_ok=True)
    
    if file_name is None:
        file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    file_handler = logging.FileHandler(log_dir / file_name)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger