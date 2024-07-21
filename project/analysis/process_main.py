import argparse
import json
from typing_extensions import BinaryIO

import yaml

from analysis import processB, processA
from analysis import processC
from config import AppConfig


def load_prompts_config(file_path: str) -> dict:
    """Load prompts configuration from a YAML file.

    Args:
        file_path (str): Path to the YAML configuration file.

    Returns:
        dict: The configuration loaded from the file.
    """
    with open(file_path) as file:
        config = yaml.safe_load(file)
    return config


def run(advert_image: bytes, advert_heatmap_image: bytes) -> list:
    """Execute the main processing pipeline using the provided configuration and image paths.

    Args:
        advert_image (BinaryIO): image file to process.
        advert_heatmap_image (BinaryIO): heatmap image file to process.

    Returns:
        list: The result of the final processing stage.
    """

    app_config = AppConfig()

    app_config.process_logger.info("Start Main process")
    a_output = processA.pipeline(app_config.prompts_config["a_process"], advert_image, advert_heatmap_image)
    b_output = processB.pipeline(app_config.prompts_config["b_process"], advert_image)
    c_output = processC.pipeline(app_config.prompts_config["c_process"], a_output, b_output)

    return json.loads(json.dumps(c_output, ensure_ascii=False, indent=4))
