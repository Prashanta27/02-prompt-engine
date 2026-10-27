from abc import ABC, abstractmethod

from asux_prompt_engine.models.prompt import PromptDefinition


class BasePromptRegistry(ABC):
    """
    Abstract interface for managing prompt definitions.
    """

    @abstractmethod
    def register(self, prompt: PromptDefinition) -> None:
        """Register a new prompt or version. Raises PromptVersionConflictError if exists."""
        pass

    @abstractmethod
    def get(self, name: str, version: str | None = None) -> PromptDefinition:
        """
        Retrieve a prompt by name.
        If version is None, retrieves the 'active' or latest version.
        Raises PromptNotFoundError if not found.
        """
        pass

    @abstractmethod
    def list_prompts(self) -> list[str]:
        """List all unique prompt names in the registry."""
        pass

    @abstractmethod
    def list_versions(self, name: str) -> list[str]:
        """List all versions for a specific prompt name."""
        pass

    @abstractmethod
    def update(self, prompt: PromptDefinition) -> None:
        """
        Update an existing prompt version.
        Raises PromptNotFoundError if the prompt version doesn't exist.
        """
        pass
