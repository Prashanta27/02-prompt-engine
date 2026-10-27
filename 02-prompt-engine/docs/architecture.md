# Architecture

The Prompt Engine serves as the centralized repository for prompt templates, isolating prompt management from business logic.

## Flow

1. Application/Agent asks `PromptEngine` to render a specific prompt by `name` and `version`.
2. `PromptEngine` queries the `PromptRegistry`.
3. `PromptRegistry` loads the `PromptDefinition` (e.g., from a YAML file).
4. `PromptEngine` passes the definition and variables to the `PromptRenderer`.
5. `PromptRenderer` validates variables and safely interpolates them via a Sandboxed Jinja2 Environment.
6. The resulting messages are mapped cleanly to `Message` objects.
7. The Application passes these messages to Project 1's `LLMClient`.
