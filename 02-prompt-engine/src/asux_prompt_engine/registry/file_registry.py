from collections import defaultdict
from pathlib import Path

import yaml

from asux_prompt_engine.exceptions.errors import (
    PromptNotFoundError,
    PromptVersionConflictError,
    RegistryStorageError,
)
from asux_prompt_engine.models.prompt import PromptDefinition
from asux_prompt_engine.registry.base import BasePromptRegistry


class FilePromptRegistry(BasePromptRegistry):
    """
    A file-backed prompt registry that stores prompts in YAML format.
    Maintains prompts in memory and syncs them to disk.
    """

    def __init__(self, storage_dir: str | Path):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # In-memory storage: name -> version -> PromptDefinition
        self._prompts: dict[str, dict[str, PromptDefinition]] = defaultdict(dict)
        self.reload()

    def _get_file_path(self, name: str, version: str) -> Path:
        safe_name = name.replace("/", "_").replace("\\", "_")
        safe_version = version.replace("/", "_").replace("\\", "_")
        return self.storage_dir / f"{safe_name}_v{safe_version}.yaml"

    def reload(self) -> None:
        """Loads all YAML files from the storage directory."""
        self._prompts.clear()

        if not self.storage_dir.exists():
            return

        for file_path in self.storage_dir.glob("*.yaml"):
            try:
                with open(file_path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)

                prompt = PromptDefinition.model_validate(data)
                self._prompts[prompt.name][prompt.version] = prompt
            except Exception as e:
                # We could log here, or raise.
                # For a rigorous registry, a corrupted file should probably raise.
                raise RegistryStorageError(f"Failed to load prompt from {file_path}: {e}") from e

    def _save_to_disk(self, prompt: PromptDefinition) -> None:
        file_path = self._get_file_path(prompt.name, prompt.version)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                # Exclude unset fields for cleaner YAML
                data = prompt.model_dump(exclude_none=True, mode="json")
                yaml.safe_dump(data, f, sort_keys=False)
        except Exception as e:
            raise RegistryStorageError(f"Failed to save prompt {prompt.name} to disk: {e}") from e

    def register(self, prompt: PromptDefinition) -> None:
        if prompt.name in self._prompts and prompt.version in self._prompts[prompt.name]:
            raise PromptVersionConflictError(
                f"Prompt '{prompt.name}' version '{prompt.version}' already exists."
            )

        self._prompts[prompt.name][prompt.version] = prompt
        self._save_to_disk(prompt)

    def get(self, name: str, version: str | None = None) -> PromptDefinition:
        if name not in self._prompts or not self._prompts[name]:
            raise PromptNotFoundError(f"Prompt '{name}' not found.")

        versions = self._prompts[name]

        if version:
            if version not in versions:
                raise PromptNotFoundError(f"Prompt '{name}' version '{version}' not found.")
            return versions[version]

        # Default active selection: lexicographical sorting, or semantic if supported.
        # Here we just take the highest sorted version.
        latest_version = sorted(versions.keys())[-1]
        return versions[latest_version]

    def list_prompts(self) -> list[str]:
        return list(self._prompts.keys())

    def list_versions(self, name: str) -> list[str]:
        if name not in self._prompts:
            raise PromptNotFoundError(f"Prompt '{name}' not found.")
        return list(self._prompts[name].keys())

    def update(self, prompt: PromptDefinition) -> None:
        if prompt.name not in self._prompts or prompt.version not in self._prompts[prompt.name]:
            raise PromptNotFoundError(
                f"Cannot update: Prompt '{prompt.name}' version '{prompt.version}' not found."
            )

        self._prompts[prompt.name][prompt.version] = prompt
        self._save_to_disk(prompt)
