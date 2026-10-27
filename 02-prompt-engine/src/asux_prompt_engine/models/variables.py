from typing import Any

from pydantic import BaseModel, Field


class PromptVariable(BaseModel):
    """
    Defines a variable required or supported by a prompt.
    """

    name: str = Field(..., description="The name of the variable (used in the template).")
    description: str | None = Field(default=None, description="What the variable represents.")
    required: bool = Field(default=True, description="Whether this variable is required.")
    default: Any | None = Field(
        default=None, description="Default value if not provided and not required."
    )
