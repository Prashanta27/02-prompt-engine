from asux_llm_gateway.models.messages import Message

from asux_prompt_engine.models.rendering import RenderRequest, RenderResult
from asux_prompt_engine.registry.base import BasePromptRegistry
from asux_prompt_engine.renderer.template_renderer import PromptRenderer


class PromptEngine:
    """
    High-level service for interacting with the Prompt Engine.
    Handles retrieving prompts from the registry and rendering them.
    """

    def __init__(self, registry: BasePromptRegistry, renderer: PromptRenderer | None = None):
        self.registry = registry
        self.renderer = renderer or PromptRenderer(strict=True)

    def render(self, request: RenderRequest) -> RenderResult:
        """
        Retrieves a prompt and renders it with the provided variables.

        Args:
            request: A RenderRequest containing the prompt name, optional version, and variables.

        Returns:
            A RenderResult containing the fully rendered messages compatible with the LLM Gateway.
        """
        # 1. Retrieve the prompt definition
        prompt_def = self.registry.get(request.name, request.version)

        # 2. Render templates
        raw_messages = self.renderer.render(prompt_def, request.variables)

        # 3. Convert to Project 1's Message models
        messages = [Message(role=msg["role"], content=msg["content"]) for msg in raw_messages]

        # 4. Construct response
        metadata = prompt_def.metadata.copy()

        return RenderResult(
            prompt_name=prompt_def.name,
            prompt_version=prompt_def.version,
            messages=messages,
            metadata=metadata,
        )
