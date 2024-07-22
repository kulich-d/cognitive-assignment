from dataclasses import dataclass, field

from langchain.output_parsers import ResponseSchema


@dataclass
class BasePrompt:
    """Dataclass for prompt description."""

    input_overview: str
    task: str
    response_schemas: list[ResponseSchema]
    role: str | None = field(default=None)

    def __init__(self, input_overview: str, task: str, response_schemas: list[dict], role: str | None = None):
        """Initialize a BasePrompt instance.

        Args:
            input_overview (str): Description of the LLM input.
            task (str): Instruction on what the LLM should do.
            response_schemas (List[dict]): List of dictionaries where each dictionary describes a response schema.
            role (Optional[str]): Description of the LLM's role.
        """
        self.input_overview = input_overview
        self.task = task
        self.response_template = [ResponseSchema(**schema) for schema in response_schemas]
        self.role = role
