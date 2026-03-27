from __future__ import annotations

from pathlib import Path
from typing import List, Literal, Optional

import yaml
from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    name: str = "gemini/gemini-flash-lite-latest"


class PromptConfig(BaseModel):
    extraction_template: str = "prompts/zero_shot_rdf.md"
    violation_translation_template: str = "prompts/two_step_correction/violation_translation.md"
    correction_template: str = "prompts/two_step_correction/correction.md"


class ShaclConfig(BaseModel):
    enabled: bool = True
    max_rounds: int = 1
    log_enabled: bool = True
    prompt_caching_enabled: bool = True


class RuntimeConfig(BaseModel):
    delay_seconds: float = 4.0


class OutputConfig(BaseModel):
    base_dir: str = "results"
    custom_tag: str = "habsburgs"
    run_dir: Optional[str] = None


class OSKGCDataConfig(BaseModel):
    data_dir: str = "OSKGC/data"
    split: str = "dev"
    ontology_dir: str = "OSKGC/ontologies/rdf"
    shacl_shapes_dir: str = "OSKGC/ontologies/shacl_shapes"


class FamilyDataConfig(BaseModel):
    input_text_file: str = "custom_family_bench/habsburgs.txt"
    ontology_file: str = "custom_family_bench/family_TBOX.owl"
    shacl_file: str = "custom_family_bench/family_TBOX_shacl_closed.ttl"


class DatasetConfig(BaseModel):
    source: Literal["custom_family_bench", "oskgc"] = "custom_family_bench"
    oskgc: OSKGCDataConfig = Field(default_factory=OSKGCDataConfig)
    custom_family_bench: FamilyDataConfig = Field(default_factory=FamilyDataConfig)


class RunConfig(BaseModel):
    model: ModelConfig = Field(default_factory=ModelConfig)
    prompts: PromptConfig = Field(default_factory=PromptConfig)
    shacl: ShaclConfig = Field(default_factory=ShaclConfig)
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    dataset: DatasetConfig = Field(default_factory=DatasetConfig)
    categories: List[str] = []

    @staticmethod
    def from_yaml(path: str) -> "RunConfig":
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return RunConfig.model_validate(data)
