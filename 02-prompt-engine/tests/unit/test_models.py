import pytest
from asux_llm_gateway.models.messages import MessageRole

from asux_prompt_engine.models.prompt import MessageTemplate, PromptDefinition
from asux_prompt_engine.models.variables import PromptVariable


def test_prompt_definition_required_variables():
    v1 = PromptVariable(name="v1", required=True)
    v2 = PromptVariable(name="v2", required=False, default="test")

    prompt = PromptDefinition(
        name="test_prompt",
        version="1.0.0",
        messages=[MessageTemplate(role=MessageRole.USER, content="{{ v1 }} {{ v2 }}")],
        variables=[v1, v2],
    )

    req_vars = prompt.required_variables
    assert len(req_vars) == 1
    assert req_vars[0].name == "v1"


def test_prompt_definition_validation_error():
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        PromptDefinition(
            name="test_prompt",
            # missing version
            messages=[],
        )
