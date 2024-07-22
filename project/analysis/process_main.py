import json

import yaml
from analysis import processB, processA
from analysis import processC
from config import AppConfig
from PIL import Image
import io


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


def resize_image_to_max_size(image_data: bytes, max_size: int):
    """
    Resizes the given image data to ensure its size does not exceed the specified max_size.

    Args:
        image_data (bytes): The original image data in bytes.
        max_size (int): The maximum allowed size for the image in bytes.

    Returns:
        bytes: The resized image data in bytes. If the original image is already within the size limit,
               the original image data is returned.
    """
    image = Image.open(io.BytesIO(image_data))

    if image.mode == 'RGBA':
        image = image.convert('RGB')

    output = io.BytesIO()
    image.save(output, format='JPEG')

    current_size = output.tell()

    if current_size <= max_size:
        return image_data

    scale_factor = (max_size / current_size) ** 0.5
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)

    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    output = io.BytesIO()
    resized_image.save(output, format='JPEG')

    return output.getvalue()


def run(advert_image: bytes, advert_heatmap_image: bytes) -> list:
    """Execute the main processing pipeline using the provided configuration and image paths.

    Args:
        advert_image (bytes): image file to process.
        advert_heatmap_image (bytes): heatmap image file to process.

    Returns:
        list: The result of the final processing stage.
    """

    app_config = AppConfig()

    if len(advert_image) > app_config.max_size:
        advert_image = resize_image_to_max_size(advert_image, app_config.max_size)

    if len(advert_heatmap_image) > app_config.max_size:
        advert_heatmap_image = resize_image_to_max_size(advert_heatmap_image, app_config.max_size)

    app_config.process_logger.info("Start Main process")
    a_output = processA.pipeline(app_config.prompts_config["a_process"], advert_image, advert_heatmap_image)
    b_output = processB.pipeline(app_config.prompts_config["b_process"], advert_image)
    c_output = processC.pipeline(app_config.prompts_config["c_process"], a_output, b_output)

    return json.loads(json.dumps(c_output, ensure_ascii=False, indent=4))
