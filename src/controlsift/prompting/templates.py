"""Canonical evaluation prompts (§25). Freeze after protocol lock.

v1.1 evidence texts are compositional packets (substance pointer, SCOPE,
ROW_DETAIL, dual sections). This template intentionally does not tutor that
grammar — discovery failures are valid experimental outcomes.
"""

from __future__ import annotations

from typing import Any, Sequence

from controlsift import LABELS

ZERO_SHOT_TEMPLATE = """You are evaluating cybersecurity control evidence.

Classify the evidence using exactly one label:

SUFFICIENT
PARTIAL
INSUFFICIENT
IRRELEVANT
CONTRADICTORY

CONTROL:
{control_statement}

ENVIRONMENT:
{environment}

EVIDENCE TYPE:
{evidence_type}

EVIDENCE:
{evidence_text}

Return valid JSON:

{{
  "label": "<LABEL>",
  "rationale": "<one concise explanation>"
}}
"""


def build_zero_shot_prompt(case: dict[str, Any]) -> str:
    return ZERO_SHOT_TEMPLATE.format(
        control_statement=case["control_statement"],
        environment=case["environment"],
        evidence_type=case["evidence_type"],
        evidence_text=case["evidence_text"],
    )


def _format_example(case: dict[str, Any]) -> str:
    return (
        f"CONTROL: {case['control_statement']}\n"
        f"ENVIRONMENT: {case['environment']}\n"
        f"EVIDENCE TYPE: {case['evidence_type']}\n"
        f"EVIDENCE: {case['evidence_text']}\n"
        f'OUTPUT: {{"label": "{case["label"]}", "rationale": "Representative {case["label"]} example."}}'
    )


def select_few_shot_examples(
    pool: Sequence[dict[str, Any]],
    *,
    labels: Sequence[str] = LABELS,
) -> list[dict[str, Any]]:
    """One fixed representative example per class from train/val only."""
    chosen: list[dict[str, Any]] = []
    for label in labels:
        candidates = sorted(
            [c for c in pool if c["label"] == label and c.get("difficulty") == "easy"],
            key=lambda c: c["id"],
        )
        if not candidates:
            candidates = sorted([c for c in pool if c["label"] == label], key=lambda c: c["id"])
        if not candidates:
            raise ValueError(f"No few-shot candidate for label {label}")
        chosen.append(candidates[0])
    return chosen


def build_few_shot_prompt(
    case: dict[str, Any],
    examples: Sequence[dict[str, Any]],
) -> str:
    demo = "\n\n".join(_format_example(ex) for ex in examples)
    return (
        "You are evaluating cybersecurity control evidence.\n\n"
        "Classify using exactly one label: "
        + ", ".join(LABELS)
        + ".\n\n"
        "Examples:\n\n"
        f"{demo}\n\n"
        "Now classify this case. Return valid JSON with keys label and rationale.\n\n"
        f"CONTROL:\n{case['control_statement']}\n\n"
        f"ENVIRONMENT:\n{case['environment']}\n\n"
        f"EVIDENCE TYPE:\n{case['evidence_type']}\n\n"
        f"EVIDENCE:\n{case['evidence_text']}\n"
    )
