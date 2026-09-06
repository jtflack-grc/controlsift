"""Evaluation runners for classical and LLM prediction files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional, Sequence

from controlsift.evaluation.metrics import compute_classification_metrics
from controlsift.evaluation.slices import slice_metrics
from controlsift.evaluation.statistics import bootstrap_macro_f1


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def evaluate_predictions(
    cases: Sequence[dict[str, Any]],
    predictions: Sequence[dict[str, Any]],
    *,
    experiment: str,
    dataset_version: str = "1.0.0",
    model: Optional[str] = None,
    seed: int = 42,
    run_bootstrap: bool = True,
) -> dict[str, Any]:
    """predictions: list of {id, pred_label} aligned or keyed by id."""
    by_id = {p["id"]: p for p in predictions}
    y_true = []
    y_pred = []
    ordered_cases = []
    for case in cases:
        if case["id"] not in by_id:
            raise KeyError(f"Missing prediction for {case['id']}")
        ordered_cases.append(case)
        y_true.append(case["label"])
        y_pred.append(by_id[case["id"]]["pred_label"])

    metrics = compute_classification_metrics(y_true, y_pred)
    payload: dict[str, Any] = {
        "experiment": experiment,
        "dataset_version": dataset_version,
        "model": model,
        "seed": seed,
        "metrics": {
            "accuracy": metrics["accuracy"],
            "macro_f1": metrics["macro_f1"],
            "macro_precision": metrics["macro_precision"],
            "macro_recall": metrics["macro_recall"],
            "weighted_f1": metrics["weighted_f1"],
            "parse_success_rate": metrics["parse_success_rate"],
            "per_class": metrics["per_class"],
            "confusion_matrix": metrics["confusion_matrix"],
            "confusion_matrix_normalized": metrics["confusion_matrix_normalized"],
            "labels": metrics["labels"],
            "n": metrics["n"],
        },
        "slices": slice_metrics(ordered_cases, y_pred),
    }
    if run_bootstrap:
        payload["bootstrap_macro_f1"] = bootstrap_macro_f1(y_true, y_pred, seed=seed)
    return payload


def save_predictions(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
