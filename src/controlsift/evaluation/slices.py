"""Slice-based performance analysis (§32)."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Sequence

from controlsift.evaluation.metrics import compute_classification_metrics


def _slice_key(case: dict[str, Any], slice_name: str) -> str:
    if slice_name == "failure_tags":
        tags = case.get("failure_tags") or []
        if not tags:
            return "(none)"
        return ",".join(sorted(tags))
    return str(case.get(slice_name, "unknown"))


def slice_metrics(
    cases: Sequence[dict[str, Any]],
    y_pred: Sequence[str],
    *,
    slice_names: Sequence[str] = ("control_domain", "evidence_type", "difficulty", "failure_tags"),
) -> dict[str, Any]:
    if len(cases) != len(y_pred):
        raise ValueError("cases and y_pred length mismatch")

    out: dict[str, Any] = {}
    for slice_name in slice_names:
        buckets: dict[str, list[int]] = defaultdict(list)
        for i, case in enumerate(cases):
            buckets[_slice_key(case, slice_name)].append(i)
        slice_report: dict[str, Any] = {}
        for key, idxs in sorted(buckets.items(), key=lambda kv: kv[0]):
            yt = [cases[i]["label"] for i in idxs]
            yp = [y_pred[i] for i in idxs]
            m = compute_classification_metrics(yt, yp)
            slice_report[key] = {
                "n": m["n"],
                "macro_f1": m["macro_f1"],
                "accuracy": m["accuracy"],
            }
        out[slice_name] = slice_report
    return out
