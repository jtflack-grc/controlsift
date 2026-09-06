#!/usr/bin/env python3
"""Aggregate evaluation artifacts and sync public docs/data/results.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Optional

from controlsift.evaluation.metrics import empty_metrics_payload

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = [
    ("majority", "majority_class"),
    ("tfidf", "tfidf_logistic_regression"),
    ("gemma_zero_shot", "google/gemma-3-1b-it"),
    ("gemma_few_shot", "google/gemma-3-1b-it"),
    ("gemma_qlora", "google/gemma-3-1b-it+qlora"),
]


def _read_metrics(path: Path) -> Optional[dict[str, Any]]:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def build_public_results() -> dict[str, Any]:
    experiments = {}
    for exp, model in EXPERIMENTS:
        payload = _read_metrics(REPO_ROOT / "results" / exp / "metrics_test.json")
        if payload is None:
            payload = empty_metrics_payload(exp, model=model)
        metrics = payload.get("metrics", {})
        experiments[exp] = {
            "experiment": exp,
            "model": payload.get("model", model),
            "dataset_version": payload.get("dataset_version", "1.0.0"),
            "seed": payload.get("seed", 42),
            "macro_f1": metrics.get("macro_f1"),
            "accuracy": metrics.get("accuracy"),
            "macro_precision": metrics.get("macro_precision"),
            "macro_recall": metrics.get("macro_recall"),
            "challenge_macro_f1": None,
        }
        chal = _read_metrics(REPO_ROOT / "results" / exp / "metrics_challenge.json")
        if chal:
            experiments[exp]["challenge_macro_f1"] = chal.get("metrics", {}).get("macro_f1")

    return {
        "dataset_version": "1.1.0",
        "primary_metric": "macro_f1",
        "status": "partial" if any(v["macro_f1"] is not None for v in experiments.values()) else "pending",
        "experiments": experiments,
        "notes": (
            "Public metrics are copied from results/*/metrics_*.json only. "
            "Null means the experiment has not been executed yet."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "docs" / "data" / "results.json",
    )
    args = parser.parse_args()
    payload = build_public_results()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    print(json.dumps({"ok": True, "status": payload["status"]}, indent=2))


if __name__ == "__main__":
    main()
