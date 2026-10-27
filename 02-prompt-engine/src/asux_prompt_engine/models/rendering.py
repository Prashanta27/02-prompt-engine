from typing import Any

from asux_llm_gateway.models.messages import Message
from pydantic import BaseModel, Field


class RenderRequest(BaseModel):
    """
    Request to render a prompt.
    """

    name: str = Field(..., description="Name of the prompt to render.")
    version: str | None = Field(
        default=None, description="Specific version to render, or latest if None."
    )
    variables: dict[str, Any] = Field(
        default_factory=dict, description="Variables to inject into the template."
    )


class RenderResult(BaseModel):
    """
    The result of rendering a prompt template.
    """

    prompt_name: str
    prompt_version: str
    messages: list[Message]
    metadata: dict[str, Any] = Field(default_factory=dict)
