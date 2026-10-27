import asyncio
import os
from pathlib import Path

# From Project 1 (Gateway)
from asux_llm_gateway.clients.llm_client import LLMClient
from asux_llm_gateway.models.requests import GatewayRequest

from asux_prompt_engine.models.rendering import RenderRequest

# From Project 2 (Prompt Engine)
from asux_prompt_engine.registry.file_registry import FilePromptRegistry
from asux_prompt_engine.services.prompt_engine import PromptEngine


async def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("NOTE: No OPENAI_API_KEY found. This example will construct the request but may fail during Gateway execution.")

    # 1. Initialize Prompt Engine
    prompts_dir = Path(__file__).parent.parent / "src" / "asux_prompt_engine" / "prompts"
    registry = FilePromptRegistry(prompts_dir)
    engine = PromptEngine(registry)

    # 2. Render the "planner" prompt
    render_req = RenderRequest(
        name="planner",
        variables={
            "goal": "Write a python script to parse logs.",
            "constraints": "Must not use external dependencies."
        }
    )
    render_result = engine.render(render_req)
    print(f"Rendered {render_result.prompt_name} (v{render_result.prompt_version}).")

    # 3. Initialize Project 1 LLMClient
    client = LLMClient()

    # 4. Construct the GatewayRequest using the fully rendered messages
    gateway_req = GatewayRequest(
        messages=render_result.messages,
        temperature=render_result.metadata.get("temperature", 0.7),
        model=render_result.metadata.get("recommended_model")
    )

    print("\n--- Sending request to Project 1 (LLM Gateway) ---")
    try:
        response = await client.complete(gateway_req)
        print("\n--- LLM Response ---")
        print(response.content)
        if response.usage:
            print(f"\n[Usage: {response.usage.total_tokens} tokens]")
    except Exception as e:
        print(f"\nGateway Execution Error: {e}")
        print("This is expected if you have not configured the Gateway with a valid OPENAI_API_KEY.")

if __name__ == "__main__":
    asyncio.run(main())
