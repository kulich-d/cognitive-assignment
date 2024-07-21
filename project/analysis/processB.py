"""This module provides functionality for processing images and generating results based on provided configurations.

It includes functions for retrieving help information from a PDF and running
the image processing pipeline.
"""
from langchain.output_parsers import StructuredOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate

from analysis import utils
from analysis.base_prompt import BasePrompt
from common import LLMException
from config.config import AppConfig


def get_help_info(process_prompts: dict) -> str:
    """Retrieves help information from a PDF document specified in the process prompts.

    Args:
        process_prompts (dict): A dictionary containing configuration information,
                                including the path to the helper document.

    Returns:
        str: The combined text content from all pages of the PDF document.
    """
    doc_path = process_prompts["helper_doc_path"]
    loader = PyPDFLoader(doc_path, extract_images=True)
    help_info = "\n".join([page.page_content for page in loader.load()])
    return help_info


def pipeline(process_prompts: dict, advert_image: bytes) -> dict:
    """Executes the processing pipeline using the provided prompts and image path.

    It retrieves help information from a PDF, constructs a chat prompt template,
    and processes the image with the LLM.

    Args:
        process_prompts (dict): A dictionary containing configuration information,
                                including prompts and instructions for processing.
        advert_image (bytes): Image file to be processed.

    Returns:
        dict: The result of the image processing, parsed into a structured format.

    Raises:
        LLMException: If an error occurs during the LLM processing.
    """
    app_config = AppConfig()
    app_config.process_logger.info("Start process B")
    help_info = get_help_info(process_prompts)
    prompt = BasePrompt(**process_prompts["b_instructions"])

    chat_template = ChatPromptTemplate.from_messages([
        ("system", prompt.role),
        ("system", "{task_instruction}"),
        ("system", "{response_template}"),
        ("system", "When completing the task, you will need the following information {help_info}"),
        (
            "user",
            [
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64,{image}"},
                }
            ],
        ),
    ])

    output_parser = StructuredOutputParser.from_response_schemas(prompt.response_template)
    chain = chat_template | app_config.model | output_parser

    base64_image = utils.encode_image(advert_image)

    try:
        result = chain.invoke(
            {"task_instruction": prompt.input_overview + "\n" + prompt.task,
             "response_template": output_parser.get_format_instructions(),
             "help_info": help_info,
             "image": base64_image})
    except Exception as e:
        raise LLMException(str(e))

    app_config.process_logger.info(result)
    return result
