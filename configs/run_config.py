from __future__ import annotations

from pathlib import Path
from typing import Literal, Optional

import yaml
from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    name: str = "gemini/gemini-flash-lite-latest"


class PromptConfig(BaseModel):
    main_system: str = "prompts/main_system.md"
    main_user: str = "prompts/main_user.md"
    translation_system: str = "prompts/translation_system.md"
    translation_user: str = "prompts/translation_user.md"


class RuntimeConfig(BaseModel):
    delay_seconds: float = 4.0
    max_iterations: int = 10
    prompt_caching_enabled: bool = False
    streaming: bool = False


class OutputConfig(BaseModel):
    base_dir: str = "results"
    custom_tag: str = "habsburgs"
    run_dir: Optional[str] = None


class DatasetConfig(BaseModel):
    source: Literal["custom_family_bench"] = "custom_family_bench"


class RunConfig(BaseModel):
    model: ModelConfig = Field(default_factory=ModelConfig)
    prompts: PromptConfig = Field(default_factory=PromptConfig)
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    dataset: DatasetConfig = Field(default_factory=DatasetConfig)

    @staticmethod
    def from_yaml(path: str) -> "RunConfig":
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return RunConfig.model_validate(data)
