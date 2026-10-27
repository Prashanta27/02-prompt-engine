from typing import Any

from asux_llm_gateway.models.messages import MessageRole
from pydantic import BaseModel, Field

from asux_prompt_engine.models.variables import PromptVariable


class MessageTemplate(BaseModel):
    """
    Template for a single message in a prompt.
    """

    role: MessageRole
    content: str = Field(
        ..., description="The template string (e.g., Jinja2 syntax) for the message."
    )


class PromptDefinition(BaseModel):
    """
    The complete definition of a prompt, including metadata, variables, and templates.
    """

    name: str = Field(..., description="Unique stable identifier for the prompt.")
    version: str = Field(..., description="Semantic version or version string.")
    description: str | None = Field(default=None, description="Purpose and intended usage.")

    # Using a list of MessageTemplates to cleanly separate system/user/assistant instructions
    messages: list[MessageTemplate] = Field(..., description="The ordered message templates.")

    variables: list[PromptVariable] = Field(
        default_factory=list, description="Variables supported by this prompt."
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Optional metadata (e.g., recommended model, max tokens)."
    )

    tags: list[str] = Field(default_factory=list, description="Categorization tags.")
    status: str = Field(default="active", description="Status (e.g., active, draft, archived).")

    @property
    def required_variables(self) -> list[PromptVariable]:
        return [v for v in self.variables if v.required]
