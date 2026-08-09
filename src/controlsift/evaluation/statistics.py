"""Statistical comparison helpers (§31)."""

from __future__ import annotations

from typing import Sequence

import numpy as np
from scipy import stats

from controlsift import LABELS
from controlsift.evaluation.metrics import compute_classification_metrics


def bootstrap_macro_f1(
    y_true: Sequence[str],
    y_pred: Sequence[str],
    *,
    n_resamples: int = 200,
    confidence_level: float = 0.95,
    seed: int = 42,
) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    y_true_arr = np.asarray(list(y_true))
    y_pred_arr = np.asarray(list(y_pred))
    n = len(y_true_arr)
    if n == 0:
        return {"macro_f1": 0.0, "ci_low": 0.0, "ci_high": 0.0}

    point = compute_classification_metrics(y_true_arr, y_pred_arr)["macro_f1"]
    scores = []
    for _ in range(n_resamples):
        idx = rng.integers(0, n, size=n)
        scores.append(
            compute_classification_metrics(y_true_arr[idx], y_pred_arr[idx])["macro_f1"]
        )
    alpha = 1 - confidence_level
    low, high = np.quantile(scores, [alpha / 2, 1 - alpha / 2])
    return {
        "macro_f1": float(point),
        "ci_low": float(low),
        "ci_high": float(high),
        "n_resamples": float(n_resamples),
    }


def bootstrap_macro_f1_delta(
    y_true: Sequence[str],
    y_pred_a: Sequence[str],
    y_pred_b: Sequence[str],
    *,
    n_resamples: int = 200,
    confidence_level: float = 0.95,
    seed: int = 42,
) -> dict[str, float]:
    """Bootstrap CI for macro-F1(B) - macro-F1(A)."""
    rng = np.random.default_rng(seed)
    y_true_arr = np.asarray(list(y_true))
    a = np.asarray(list(y_pred_a))
    b = np.asarray(list(y_pred_b))
    n = len(y_true_arr)
    point = (
        compute_classification_metrics(y_true_arr, b)["macro_f1"]
        - compute_classification_metrics(y_true_arr, a)["macro_f1"]
    )
    deltas = []
    for _ in range(n_resamples):
        idx = rng.integers(0, n, size=n)
        fa = compute_classification_metrics(y_true_arr[idx], a[idx])["macro_f1"]
        fb = compute_classification_metrics(y_true_arr[idx], b[idx])["macro_f1"]
        deltas.append(fb - fa)
    alpha = 1 - confidence_level
    low, high = np.quantile(deltas, [alpha / 2, 1 - alpha / 2])
    return {
        "delta_macro_f1": float(point),
        "ci_low": float(low),
        "ci_high": float(high),
        "n_resamples": float(n_resamples),
    }


def mcnemar_test(
    y_true: Sequence[str],
    y_pred_a: Sequence[str],
    y_pred_b: Sequence[str],
) -> dict[str, float]:
    """McNemar test on paired correct/incorrect predictions."""
    yt = list(y_true)
    a_correct = [p == t for p, t in zip(y_pred_a, yt)]
    b_correct = [p == t for p, t in zip(y_pred_b, yt)]
    n01 = sum(1 for ac, bc in zip(a_correct, b_correct) if ac and not bc)
    n10 = sum(1 for ac, bc in zip(a_correct, b_correct) if (not ac) and bc)
    # Continuity-corrected McNemar
    statistic = (abs(n01 - n10) - 1) ** 2 / (n01 + n10) if (n01 + n10) > 0 else 0.0
    pvalue = float(stats.chi2.sf(statistic, df=1)) if (n01 + n10) > 0 else 1.0
    return {
        "n01_a_correct_b_wrong": float(n01),
        "n10_a_wrong_b_correct": float(n10),
        "statistic": float(statistic),
        "pvalue": pvalue,
        "labels_considered": float(len(LABELS)),
    }
