from pathlib import Path

import pytest

from asux_prompt_engine.models.rendering import RenderRequest
from asux_prompt_engine.registry.file_registry import FilePromptRegistry
from asux_prompt_engine.services.prompt_engine import PromptEngine


@pytest.fixture
def builtin_registry() -> FilePromptRegistry:
    # Point to the actual built-in prompts directory
    prompts_dir = Path(__file__).parent.parent.parent / "src" / "asux_prompt_engine" / "prompts"
    return FilePromptRegistry(prompts_dir)


def test_builtin_prompts_loaded(builtin_registry: FilePromptRegistry):
    prompts = builtin_registry.list_prompts()
    assert "sales_assistant" in prompts
    assert "support_assistant" in prompts
    assert "planner" in prompts
    assert "reviewer" in prompts


def test_sales_assistant_rendering(builtin_registry: FilePromptRegistry):
    engine = PromptEngine(registry=builtin_registry)

    req = RenderRequest(
        name="sales_assistant",
        variables={"catalog_context": "Item A is $10."},  # customer_name is optional
    )
    result = engine.render(req)

    assert len(result.messages) == 2
    assert result.messages[0].role == "system"
    assert "Item A is $10" in result.messages[0].content
    assert result.messages[1].role == "user"
    assert "Customer" in result.messages[1].content  # Default value applied


def test_support_assistant_rendering(builtin_registry: FilePromptRegistry):
    engine = PromptEngine(registry=builtin_registry)

    req = RenderRequest(
        name="support_assistant",
        variables={"customer_issue": "Broken screen", "knowledge_base_context": "No refunds"},
    )
    result = engine.render(req)
    assert len(result.messages) == 2
    assert "Broken screen" in result.messages[1].content
    assert "No refunds" in result.messages[0].content
