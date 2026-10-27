
import pytest
from asux_llm_gateway.models.messages import MessageRole

from asux_prompt_engine.exceptions.errors import PromptNotFoundError, PromptVersionConflictError
from asux_prompt_engine.models.prompt import MessageTemplate, PromptDefinition
from asux_prompt_engine.registry.file_registry import FilePromptRegistry


@pytest.fixture
def dummy_prompt() -> PromptDefinition:
    return PromptDefinition(
        name="dummy",
        version="1.0.0",
        messages=[MessageTemplate(role=MessageRole.USER, content="test")],
    )


def test_registry_register_and_get(
    file_registry: FilePromptRegistry, dummy_prompt: PromptDefinition
):
    file_registry.register(dummy_prompt)

    retrieved = file_registry.get("dummy", "1.0.0")
    assert retrieved.name == "dummy"

    # Test file was written
    assert (file_registry.storage_dir / "dummy_v1.0.0.yaml").exists()


def test_registry_duplicate_registration(
    file_registry: FilePromptRegistry, dummy_prompt: PromptDefinition
):
    file_registry.register(dummy_prompt)
    with pytest.raises(PromptVersionConflictError):
        file_registry.register(dummy_prompt)


def test_registry_get_not_found(file_registry: FilePromptRegistry):
    with pytest.raises(PromptNotFoundError):
        file_registry.get("nonexistent")


def test_registry_default_active_version(
    file_registry: FilePromptRegistry, dummy_prompt: PromptDefinition
):
    file_registry.register(dummy_prompt)

    v2 = dummy_prompt.model_copy(update={"version": "2.0.0"})
    file_registry.register(v2)

    # get without version should return highest lexicographically
    active = file_registry.get("dummy")
    assert active.version == "2.0.0"


def test_registry_reload_from_disk(
    file_registry: FilePromptRegistry, dummy_prompt: PromptDefinition
):
    file_registry.register(dummy_prompt)

    # Create new instance to force reload from disk
    new_registry = FilePromptRegistry(file_registry.storage_dir)
    loaded = new_registry.get("dummy")
    assert loaded.version == "1.0.0"
