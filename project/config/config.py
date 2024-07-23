import os

import yaml
from common import logger
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


class AppConfig:
    """Singleton class to handle application configuration.

    This class initializes the logger and loads environment variables from a .env file.
    It also sets up the OpenAI model to be used in the application.
    """
    _instance = None

    def __new__(cls, env_path="./envs/.env", logger_save_path=".", prompts_config_path="", *args, **kwargs):
        """Create or return the singleton instance of AppConfig.

        Args:
            env_path (str): Path to the .env file. Defaults to './envs/.env'.
            logger_save_path (str): Path to the logger file. Defaults is main.py folder.
            *args: Additional positional arguments to pass to the parent class's __new__ method.
            **kwargs: Additional keyword arguments to pass to the parent class's __new__ method.

        Returns:
            AppConfig: The singleton instance of the AppConfig class.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.__initialize(env_path, logger_save_path, prompts_config_path)
        return cls._instance

    def __initialize(self, env_path: str, logger_save_path: str, prompts_config_path: str):
        """Initialize the configuration by loading environment variables and setting up the model.

        Args:
            env_path (str): Path to the .env file to load environment variables from.
            logger_save_path (str): Path to the logger file. Defaults is main.py folder.
            prompt_config_path (str): Path to .yaml prompts config

        Raises:
            FileNotFoundError: If the specified .env file is not found.
            Exception: For any errors that occur during model initialization.
        """
        self.port = int(os.getenv("PORT", 8000))
        self.max_size = 30000  # max image size in bytes; used to ensure the image size does not exceed the context window limit of the model

        with open(prompts_config_path) as file:
            self.prompts_config = yaml.safe_load(file)

        self.process_logger = logger.get_logger(logger_save_path, 'Logger for process')
        load_dotenv(env_path)

        try:
            # self.model = ChatOpenAI(model="gpt-4o-mini")
            self.model = ChatOpenAI(model="gpt-4o")
        except Exception as e:
            self.process_logger.error(f"Error initializing ChatOpenAI model: {e}")
            raise
