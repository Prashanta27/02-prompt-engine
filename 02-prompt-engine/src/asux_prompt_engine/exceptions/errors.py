class PromptEngineError(Exception):
    """Base exception for all Prompt Engine errors."""

    pass


class PromptNotFoundError(PromptEngineError):
    """Raised when a prompt name or version is not found in the registry."""

    pass


class PromptVersionConflictError(PromptEngineError):
    """Raised when trying to register a prompt version that already exists."""

    pass


class PromptValidationError(PromptEngineError):
    """Raised when a prompt definition is invalid."""

    pass


class VariableMissingError(PromptEngineError):
    """Raised when a required variable is missing during rendering."""

    pass


class UnexpectedVariableError(PromptEngineError):
    """Raised when an unexpected variable is provided during rendering."""

    pass


class TemplateRenderingError(PromptEngineError):
    """Raised when the template engine fails to render the content."""

    pass


class RegistryStorageError(PromptEngineError):
    """Raised when the prompt registry fails to read or write data."""

    pass
