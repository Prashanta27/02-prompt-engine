from typing import Any

import jinja2
from jinja2.sandbox import SandboxedEnvironment

from asux_prompt_engine.exceptions.errors import (
    TemplateRenderingError,
    UnexpectedVariableError,
    VariableMissingError,
)
from asux_prompt_engine.models.prompt import PromptDefinition


class PromptRenderer:
    """
    Safely renders prompt templates using Jinja2 SandboxedEnvironment.
    """

    def __init__(self, strict: bool = True):
        # SandboxedEnvironment prevents arbitrary Python execution
        # undefined=jinja2.StrictUndefined ensures missing variables raise an error
        self.env = SandboxedEnvironment(
            undefined=jinja2.StrictUndefined if strict else jinja2.Undefined,
            autoescape=False,  # We are rendering plain text, not HTML
        )
        self.strict = strict

    def render(self, prompt: PromptDefinition, variables: dict[str, Any]) -> list[dict[str, str]]:
        """
        Renders a PromptDefinition into a list of messages.

        Args:
            prompt: The prompt definition to render.
            variables: Dictionary of variable values.

        Returns:
            A list of dicts, each with 'role' and 'content' keys.
        """
        # 1. Variable validation
        provided_keys = set(variables.keys())
        expected_keys = {v.name for v in prompt.variables}

        # Check required variables
        for var in prompt.required_variables:
            if var.name not in provided_keys:
                raise VariableMissingError(
                    f"Missing required variable '{var.name}' for prompt '{prompt.name}'."
                )

        # Inject default values for missing optional variables
        final_vars = {}
        for var in prompt.variables:
            if var.name in provided_keys:
                final_vars[var.name] = variables[var.name]
            else:
                final_vars[var.name] = var.default

        # Check unexpected variables if strict
        if self.strict:
            unexpected = provided_keys - expected_keys
            if unexpected:
                raise UnexpectedVariableError(
                    f"Unexpected variables provided for prompt '{prompt.name}': {unexpected}"
                )
        else:
            # Still merge unexpected ones in if not strict
            for k in provided_keys - expected_keys:
                final_vars[k] = variables[k]

        # 2. Render templates
        rendered_messages = []
        for msg_tpl in prompt.messages:
            try:
                template = self.env.from_string(msg_tpl.content)
                rendered_content = template.render(**final_vars)

                rendered_messages.append({"role": msg_tpl.role.value, "content": rendered_content})
            except jinja2.UndefinedError as e:
                # Catch jinja2 strict undefined errors that might have slipped through
                # (e.g. accessing a property of a variable that is missing)
                raise VariableMissingError(f"Variable missing during rendering: {e}") from e
            except jinja2.TemplateError as e:
                raise TemplateRenderingError(
                    f"Failed to render template for role {msg_tpl.role}: {e}"
                ) from e

        return rendered_messages
