"""This module provides functionality for processing images and generating results based on provided сonfigurations.

It includes functions for managing session history and running image processing
with prompt-based configurations.
"""

from analysis import utils
from analysis.base_prompt import BasePrompt
from common import LLMException
from config import AppConfig
from langchain.output_parsers import StructuredOutputParser
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

# In-memory store for session histories
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Retrieves the chat message history for a given session.

    If the session does not exist, a new session history is created and added to the store.

    Args:
        session_id (str): The unique identifier for the session. Each session_id
                          should be unique for every session.

    Returns:
        BaseChatMessageHistory: The chat message history associated with the session_id.
                                 If the session_id is not found in the store, a new
                                 InMemoryChatMessageHistory instance is created and returned.

    """
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


def run_process(image_path: str, prompt: BasePrompt, chat_template: ChatPromptTemplate, session_config: dict) -> dict:
    """Runs the image processing pipeline with the given prompt and configuration.

    Args:
        image_path (str): Path to the image file to be processed.
        prompt (BasePrompt): The prompt containing instructions for the LLM.
        chat_template (ChatPromptTemplate): Template for creating the chat prompt.
        session_config (dict): Configuration dictionary for the session.

    Returns:
        dict: The result of the LLM processing, parsed into a structured format.

    Raises:
        LLMException: If an error occurs during the LLM processing.
    """
    app_config = AppConfig()
    output_parser = StructuredOutputParser.from_response_schemas(prompt.response_template)
    chain = chat_template | app_config.model
    with_message_history = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="image",
                                                      history_messages_key="history")

    base64_image = utils.encode_image(image_path)

    try:
        result = with_message_history.invoke(
            {"prompt_role": prompt.role,
             "task_instruction": prompt.input_overview + "\n" + prompt.task,
             "response_template": output_parser.get_format_instructions(),
             "image": base64_image},
            config=session_config)
        result = output_parser.parse(result.content)  # Here to be able to drop the entire line as a memory.
    except Exception as e:
        raise LLMException(str(e))

    return result


def pipeline(process_prompts: dict, image_path: str, heatmap_image_path: str) -> dict:
    """Executes the processing pipeline with the provided prompts and image paths.

    Args:
        process_prompts (dict): Dictionary containing prompts and instructions for the processing stages.
        image_path (str): Path to the image file for the first processing stage.
        heatmap_image_path (str): Path to the image file for the second processing stage.

    Returns:
        dict: The combined result of both processing stages.

    Raises:
        LLMException: If an error occurs during the LLM processing.
    """
    app_config = AppConfig()
    session_config = {"configurable": {"session_id": "procA"}}

    app_config.process_logger.info("Start process A")
    a1_prompt = BasePrompt(**process_prompts["a1_instructions"])
    a2_prompt = BasePrompt(**process_prompts["a2_instructions"])

    chat_template = ChatPromptTemplate.from_messages([ # tdo change prompt потому что оно скорее на свои штуки отвлекается чем на картинку, показать эксперимент со второй картинкой
        ("system", "{prompt_role}"),
        ("system", "{task_instruction}"),
        ("system", "{response_template}"),
        MessagesPlaceholder(variable_name="history"),
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

    app_config.process_logger.info("Start process A1")
    a1 = run_process(image_path, a1_prompt, chat_template, session_config)

    app_config.process_logger.info("Start process A2")
    a2 = run_process(heatmap_image_path, a2_prompt, chat_template, session_config)

    result = a1 | a2
    app_config.process_logger.info(result)
    return result
