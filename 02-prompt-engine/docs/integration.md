# Integration with LLM Gateway

This project integrates cleanly with `asux-llm-gateway` (Project 1).

## Request Flow
Rather than formatting strings manually, future projects (like the Tool Runtime) should use the Prompt Engine to generate fully formed `asux_llm_gateway.models.messages.Message` instances.

```python
from asux_prompt_engine.services.prompt_engine import PromptEngine
from asux_prompt_engine.models.rendering import RenderRequest
from asux_llm_gateway.clients.llm_client import LLMClient
from asux_llm_gateway.models.requests import GatewayRequest

# 1. Render Prompt
render_result = engine.render(RenderRequest(
    name="planner",
    variables={"goal": "Parse logs."}
))

# 2. Convert to Gateway Request
req = GatewayRequest(messages=render_result.messages)

# 3. Call Gateway
client = LLMClient()
response = await client.complete(req)
```
