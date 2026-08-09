"""Load and validate QLoRA training configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yaml_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if not isinstance(cfg, dict):
        raise ValueError(f"Config must be a mapping: {path}")
    return cfg


def resolve_lora_target_modules(model) -> list[str]:
    """Inspect a loaded HF model and return plausible LoRA linear module names.

    Do not hard-code module names from unrelated architectures.
    """
    candidates = {
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    }
    found: set[str] = set()
    for name, module in model.named_modules():
        leaf = name.rsplit(".", 1)[-1]
        if leaf in candidates and module.__class__.__name__ in {
            "Linear",
            "Linear8bitLt",
            "Linear4bit",
        }:
            found.add(leaf)
    if not found:
        raise RuntimeError(
            "Could not infer LoRA target modules from model; inspect architecture manually."
        )
    # Prefer attention projections when present
    preferred = [m for m in ("q_proj", "k_proj", "v_proj", "o_proj") if m in found]
    if preferred:
        return preferred
    return sorted(found)
