class LLMException(Exception):
    """Custom exception class for handling errors specific to the LLM (Large Language Model) process.

    Inherits from the built-in Exception class and allows for custom error messages.
    """

    def __init__(self, message: str):
        """Initializes the LLMException with a custom error message.

        Args:
           message (str): The error message to be associated with the exception.
        """
        super().__init__(message)
        self.message = message

    def __str__(self):
        """Returns the string representation of the exception.

        Returns:
            str: The error message associated with the exception.
        """
        return f"{self.message}"
