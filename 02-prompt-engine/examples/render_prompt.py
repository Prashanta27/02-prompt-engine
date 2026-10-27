from pathlib import Path

from asux_prompt_engine.models.rendering import RenderRequest
from asux_prompt_engine.registry.file_registry import FilePromptRegistry
from asux_prompt_engine.services.prompt_engine import PromptEngine


def main():
    # 1. Initialize registry with built-in prompts
    prompts_dir = Path(__file__).parent.parent / "src" / "asux_prompt_engine" / "prompts"
    registry = FilePromptRegistry(prompts_dir)

    # 2. Initialize prompt engine
    engine = PromptEngine(registry)

    # 3. Define rendering request
    # This automatically validates variables against the prompt's definition
    req = RenderRequest(
        name="sales_assistant",
        variables={
            "customer_name": "Alice",
            "catalog_context": "- Product A: $500\n- Product B: $800",
        },
    )

    # 4. Render the prompt messages
    result = engine.render(req)

    # 5. Inspect the selected version and rendered messages
    print(f"Rendered Prompt: {result.prompt_name} (v{result.prompt_version})")
    print("-" * 40)
    for msg in result.messages:
        print(f"[{msg.role.upper()}]:\n{msg.content}\n")


if __name__ == "__main__":
    main()
