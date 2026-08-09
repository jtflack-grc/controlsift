"""Classification metrics for ControlSift (primary: macro F1)."""

from __future__ import annotations

from typing import Any, Iterable, Optional, Sequence

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)

from controlsift import LABELS, UNPARSEABLE


def compute_classification_metrics(
    y_true: Sequence[str],
    y_pred: Sequence[str],
    *,
    labels: Sequence[str] = LABELS,
    unparseable: str = UNPARSEABLE,
) -> dict[str, Any]:
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred length mismatch")

    y_true_arr = np.asarray(list(y_true))
    y_pred_arr = np.asarray(list(y_pred))
    parse_success = float(np.mean(y_pred_arr != unparseable)) if len(y_pred_arr) else 0.0

    # Map unparseable to a dedicated bucket excluded from class labels for F1,
    # but counted as incorrect vs true labels via replacing with __UNPARSEABLE__
    # that is not in labels — sklearn will ignore unknown in average if we
    # coerce unparseable predictions to a wrong sentinel not equal to truth.
    coerced = np.array(
        [p if p in labels else f"__{unparseable}__" for p in y_pred_arr],
        dtype=object,
    )

    precision, recall, f1, support = precision_recall_fscore_support(
        y_true_arr,
        coerced,
        labels=list(labels),
        average=None,
        zero_division=0,
    )
    per_class = {
        label: {
            "precision": float(precision[i]),
            "recall": float(recall[i]),
            "f1": float(f1[i]),
            "support": int(support[i]),
        }
        for i, label in enumerate(labels)
    }
    macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(
        y_true_arr,
        coerced,
        labels=list(labels),
        average="macro",
        zero_division=0,
    )
    weighted_f1 = float(
        f1_score(y_true_arr, coerced, labels=list(labels), average="weighted", zero_division=0)
    )
    acc = float(accuracy_score(y_true_arr, coerced))
    cm = confusion_matrix(y_true_arr, coerced, labels=list(labels)).tolist()
    cm_norm = confusion_matrix(
        y_true_arr, coerced, labels=list(labels), normalize="true"
    ).tolist()

    return {
        "accuracy": acc,
        "macro_f1": float(macro_f1),
        "macro_precision": float(macro_p),
        "macro_recall": float(macro_r),
        "weighted_f1": weighted_f1,
        "per_class": per_class,
        "confusion_matrix": cm,
        "confusion_matrix_normalized": cm_norm,
        "labels": list(labels),
        "parse_success_rate": parse_success,
        "n": int(len(y_true_arr)),
    }


def empty_metrics_payload(
    experiment: str,
    *,
    dataset_version: str = "1.0.0",
    model: Optional[str] = None,
    seed: int = 42,
) -> dict[str, Any]:
    """Integrity-safe null metrics before an experiment runs (§48)."""
    return {
        "experiment": experiment,
        "dataset_version": dataset_version,
        "model": model,
        "seed": seed,
        "metrics": {
            "accuracy": None,
            "macro_f1": None,
            "macro_precision": None,
            "macro_recall": None,
        },
    }


def majority_baseline_predictions(
    y_train: Iterable[str],
    n_predict: int,
) -> list[str]:
    counts = {}
    for y in y_train:
        counts[y] = counts.get(y, 0) + 1
    majority = max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
    return [majority] * n_predict
