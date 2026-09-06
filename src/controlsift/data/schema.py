"""Dataset schema for ControlSift evidence cases (charter §18)."""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator

LABELS = (
    "SUFFICIENT",
    "PARTIAL",
    "INSUFFICIENT",
    "IRRELEVANT",
    "CONTRADICTORY",
)

SPLITS = ("train", "validation", "test", "challenge")

DIFFICULTIES = ("easy", "medium", "hard")

REVIEW_STATUSES = ("unreviewed", "reviewed", "corrected")

# Fields allowed in model prompts — never leak hidden analytical metadata.
MODEL_INPUT_FIELDS = (
    "control_statement",
    "environment",
    "evidence_type",
    "evidence_text",
)


class Label(str, Enum):
    SUFFICIENT = "SUFFICIENT"
    PARTIAL = "PARTIAL"
    INSUFFICIENT = "INSUFFICIENT"
    IRRELEVANT = "IRRELEVANT"
    CONTRADICTORY = "CONTRADICTORY"


class EvidenceCase(BaseModel):
    id: str
    scenario_family_id: str
    variant_id: str
    control_domain: str
    control_statement: str
    environment: str
    evidence_type: str
    evidence_text: str
    label: Label
    failure_tags: list[str] = Field(default_factory=list)
    difficulty: str = "medium"
    generation_method: str = "synthetic_rule_based"
    review_status: str = "unreviewed"
    split: str

    # Optional analytical metadata — must not enter model input.
    artifact_age_days: Optional[int] = None
    population_expected: Optional[int] = None
    population_observed: Optional[int] = None
    control_objective: Optional[str] = None
    source_system: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("difficulty")
    @classmethod
    def _check_difficulty(cls, v: str) -> str:
        if v not in DIFFICULTIES:
            raise ValueError(f"difficulty must be one of {DIFFICULTIES}")
        return v

    @field_validator("review_status")
    @classmethod
    def _check_review(cls, v: str) -> str:
        if v not in REVIEW_STATUSES:
            raise ValueError(f"review_status must be one of {REVIEW_STATUSES}")
        return v

    @field_validator("split")
    @classmethod
    def _check_split(cls, v: str) -> str:
        if v not in SPLITS:
            raise ValueError(f"split must be one of {SPLITS}")
        return v

    def model_input_dict(self) -> dict[str, str]:
        return {k: getattr(self, k) for k in MODEL_INPUT_FIELDS}

    def to_jsonl_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json", exclude_none=True)


def parse_case(raw: dict[str, Any]) -> EvidenceCase:
    return EvidenceCase.model_validate(raw)
