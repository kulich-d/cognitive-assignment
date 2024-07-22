import logging
import os
import sys
from datetime import datetime


def get_logger(file_path: str, name: str) -> logging.Logger:
    """Creates and configures a logger with both file and console handlers.

    Args:
        file_path (str): The path to save logger file.
        name (str): The name of the logger.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.DEBUG)
    logger.handlers.clear()

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - [%(processName)s] - [%(threadName)s] - %(levelname)s - %(message)s ',
        datefmt='"%Y-%m-%d %H:%M:%S"')

    file_handler = logging.FileHandler(
        filename=os.path.join(file_path, f'{name}_{datetime.now().strftime("%Y_%m_%d_%H_%M")}.log'),
        mode='a')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    return logger
