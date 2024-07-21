import argparse
import json

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


def main(prompts_config: dict, image_path: str, heatmap_image_path: str) -> list:
    """Execute the main processing pipeline using the provided configuration and image paths.

    Args:
        prompts_config (dict): Dictionary containing process configurations.
        image_path (str): Path to the image file to process.
        heatmap_image_path (str): Path to the heatmap image file to process.

    Returns:
        list: The result of the final processing stage.
    """
    app_config = AppConfig()
    app_config.process_logger.info("Start Main process")
    a_output = processA.pipeline(prompts_config["a_process"], image_path, heatmap_image_path)
    b_output = processB.pipeline(prompts_config["b_process"], image_path)
    c_output = processC.pipeline(prompts_config["c_process"], a_output, b_output)

    return c_output


def create_valid_json(result: list) -> str:
    """Convert the result list to a formatted JSON string.

    Args:
        result (list): The result to be converted to JSON.
    """
    return json.dumps(result, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Main')
    parser.add_argument('--env_path', type=str, default="./envs/.env")
    parser.add_argument('--logger_save_path', type=str, default=".")
    parser.add_argument('--heatmap_image_path', type=str, required=True)
    parser.add_argument('--image_path', type=str, required=True)
    args = parser.parse_args()
    prompts_config = load_prompts_config('analysis/prompts/data.yaml')
    app_config = AppConfig(args.env_path, args.logger_save_path)

    result = main(prompts_config, args.image_path, args.heatmap_image_path)
    result = create_valid_json(result)
    app_config.process_logger.info(result)  # TODO: remove
