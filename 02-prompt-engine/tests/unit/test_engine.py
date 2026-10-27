from pathlib import Path

from asux_prompt_engine.models.rendering import RenderRequest
from asux_prompt_engine.registry.file_registry import FilePromptRegistry
from asux_prompt_engine.services.prompt_engine import PromptEngine


def test_prompt_engine_render(file_registry: FilePromptRegistry, tmp_path: Path):
    from asux_llm_gateway.models.messages import MessageRole

    from asux_prompt_engine.models.prompt import MessageTemplate, PromptDefinition
    from asux_prompt_engine.models.variables import PromptVariable

    prompt = PromptDefinition(
        name="test",
        version="1.0",
        variables=[PromptVariable(name="name", required=True)],
        messages=[MessageTemplate(role=MessageRole.USER, content="Hello {{ name }}")],
    )
    file_registry.register(prompt)

    engine = PromptEngine(registry=file_registry)

    req = RenderRequest(name="test", variables={"name": "Bob"})
    result = engine.render(req)

    assert result.prompt_name == "test"
    assert len(result.messages) == 1
    assert result.messages[0].role == "user"
    assert result.messages[0].content == "Hello Bob"
