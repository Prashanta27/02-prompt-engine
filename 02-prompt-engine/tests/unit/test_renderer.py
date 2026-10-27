import pytest
from asux_llm_gateway.models.messages import MessageRole

from asux_prompt_engine.exceptions.errors import (
    TemplateRenderingError,
    UnexpectedVariableError,
    VariableMissingError,
)
from asux_prompt_engine.models.prompt import MessageTemplate, PromptDefinition
from asux_prompt_engine.models.variables import PromptVariable
from asux_prompt_engine.renderer.template_renderer import PromptRenderer


@pytest.fixture
def sample_prompt() -> PromptDefinition:
    return PromptDefinition(
        name="hello_prompt",
        version="1.0.0",
        variables=[
            PromptVariable(name="name", required=True),
            PromptVariable(name="greeting", required=False, default="Hello"),
        ],
        messages=[MessageTemplate(role=MessageRole.USER, content="{{ greeting }}, {{ name }}!")],
    )


def test_render_success(sample_prompt):
    renderer = PromptRenderer(strict=True)
    result = renderer.render(sample_prompt, {"name": "Alice"})

    assert len(result) == 1
    assert result[0]["role"] == "user"
    assert result[0]["content"] == "Hello, Alice!"


def test_render_missing_required(sample_prompt):
    renderer = PromptRenderer(strict=True)
    with pytest.raises(VariableMissingError, match="Missing required variable 'name'"):
        renderer.render(sample_prompt, {})


def test_render_unexpected_variable(sample_prompt):
    renderer = PromptRenderer(strict=True)
    with pytest.raises(UnexpectedVariableError):
        renderer.render(sample_prompt, {"name": "Alice", "extra": "bad"})


def test_render_non_strict(sample_prompt):
    renderer = PromptRenderer(strict=False)
    # Should not raise
    result = renderer.render(sample_prompt, {"name": "Alice", "extra": "allowed"})
    assert result[0]["content"] == "Hello, Alice!"


def test_render_no_code_execution():
    renderer = PromptRenderer()

    bad_prompt = PromptDefinition(
        name="bad",
        version="1.0.0",
        variables=[],
        messages=[
            MessageTemplate(
                role=MessageRole.USER, content="{{ ''.__class__.__mro__[1].__subclasses__() }}"
            )
        ],
    )

    with pytest.raises(TemplateRenderingError):
        # Jinja2 SandboxedEnvironment restricts access to sensitive attributes like __class__
        renderer.render(bad_prompt, {})
