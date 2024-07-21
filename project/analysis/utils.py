"""This module provides utility functions for image processing, including resizing and encoding images."""
import base64
from typing_extensions import BinaryIO


def resize_image(image_path: str, output_path: str, scale_factor: int):
    """Resizes an image by a given scale factor and saves the resized image to the specified output path.

    Args:
        image_path (str): The path to the input image file that needs to be resized.
        output_path (str): The path where the resized image will be saved.
        scale_factor (int): The factor by which to scale down the image. For example, a scale factor of 2
                            will reduce the image dimensions by half.
    """
    from PIL import Image
    img = Image.open(image_path)
    width, height = img.size
    new_width = width // scale_factor
    new_height = height // scale_factor
    img = img.resize((new_width, new_height), Image.LANCZOS)
    img.save(output_path)


def encode_image(image: bytes) -> str:
    """Encodes an image file to a base64-encoded string.

    Args:
        image_path (bytes): Image file that needs to be encoded.

    Returns:
        str: The base64-encoded string of the image file.
    """
    return base64.b64encode(image).decode('utf-8');
