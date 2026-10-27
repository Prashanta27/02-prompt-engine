from pathlib import Path

import pytest

from asux_prompt_engine.registry.file_registry import FilePromptRegistry


@pytest.fixture
def test_storage_dir(tmp_path: Path) -> Path:
    return tmp_path / "prompts"


@pytest.fixture
def file_registry(test_storage_dir: Path) -> FilePromptRegistry:
    return FilePromptRegistry(test_storage_dir)
