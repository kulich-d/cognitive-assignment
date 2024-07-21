"""This module provides functionality for processing outputs from different stages.

It includes a function for executing the final processing stage of the pipeline.
"""

from langchain.output_parsers import StructuredOutputParser
from langchain_core.prompts import ChatPromptTemplate

from analysis.base_prompt import BasePrompt
from common import LLMException
from config.config import AppConfig


def pipeline(process_prompts: dict, a_output: dict, b_output: dict) -> list:
    """Executes the final processing stage using the provided prompts and outputs from previous stages.

    Args:
        process_prompts (dict): A dictionary containing prompts and instructions for the processing stages.
                                Specifically, it should include "c_instructions" with details for this stage.
        a_output (dict): The output from the first processing stage, used as input to this stage.
        b_output (dict): The output from the second processing stage, used as input to this stage.

    Returns:
        list: A list containing the result of the final processing stage.

    Raises:
            LLMException: If an error occurs during the LLM processing.
    """
    app_config = AppConfig()

    app_config.process_logger.info("Start process C")
    prompt = BasePrompt(**process_prompts["c_instructions"])

    chat_template = ChatPromptTemplate.from_messages([
        ("system", prompt.role),
        ("system", "{task_instruction}"),
        ("system", "{response_template}"),
        (
            "user", "First multi-modal LLM output {first_output}. Second multi-modal LLM output {second_output}."
        ),
    ])

    output_parser = StructuredOutputParser.from_response_schemas(prompt.response_template)
    chain = chat_template | app_config.model | output_parser

    try:
        dict_result = chain.invoke(
            {"task_instruction": prompt.input_overview + "\n" + prompt.task,
             "response_template": output_parser.get_format_instructions(),
             "first_output": a_output,
             "second_output": b_output})
    except Exception as e:
        raise LLMException(str(e))

    list_result = [dict_result]
    return list_result
