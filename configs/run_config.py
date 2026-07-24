from __future__ import annotations

from pathlib import Path
from typing import Literal, Optional

import yaml
from pydantic import BaseModel, Field, model_validator


class ModelConfig(BaseModel):
    """Configuration for the LLM used in the pipeline.

    - `name`: model identifier
    - `temperature`: sampling temperature
    - `max_retries`: retry attempts for transient failures
    """
    name: str = "gemini/gemini-flash-lite-latest"
    temperature: float = 0.0
    max_retries: int = 4


class PromptConfig(BaseModel):
    """Paths to prompt templates used by the agent and translators."""
    main_system: str = "prompts/main_system.md"
    main_system_without_shacl: str = "prompts/main_system_without_shacl.md"
    main_user: str = "prompts/main_user.md"
    translation_system: str = "prompts/translation_system.md"
    translation_user: str = "prompts/translation_user.md"
    not_typed: str = "prompts/not_typed.md"


class RuntimeConfig(BaseModel):
    delay_seconds: float = 4.0
    max_iterations: int = 10
    min_iterations: int = 5
    prompt_caching_enabled: bool = False
    shacl_validation: bool = True
    violation_translation: bool = True
    same_data_graph: bool = False
    async_mode: bool = False
    enforce_shacl: bool = True

    @model_validator(mode="before")
    @classmethod
    def map_async_key(cls, data):
        if isinstance(data, dict) and "async" in data and "async_mode" not in data:
            data = data.copy()
            data["async_mode"] = data["async"]
        return data


class OutputConfig(BaseModel):
    """Output directory configuration for run artifacts."""
    base_dir: str = "results"
    custom_tag: str = "habsburgs"
    run_dir: Optional[str] = None


class DatasetConfig(BaseModel):
    """Which dataset loader to use for the run."""
    source: Literal["custom_family_bench", "example_run", "shacl_repair"] = "example_run"


class RunConfig(BaseModel):
    model: ModelConfig = Field(default_factory=ModelConfig)
    prompts: PromptConfig = Field(default_factory=PromptConfig)
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    dataset: DatasetConfig = Field(default_factory=DatasetConfig)

    @staticmethod
    def from_yaml(path: str) -> "RunConfig":
        """Load a RunConfig from a YAML file and validate it.

        Raises `FileNotFoundError` if the path does not exist.
        """
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return RunConfig.model_validate(data)
