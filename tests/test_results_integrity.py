"""Public metrics must not invent non-null scores without result files."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_public_results_match_machine_files():
    public = json.loads((REPO / "docs" / "data" / "results.json").read_text(encoding="utf-8"))
    for exp, row in public["experiments"].items():
        metrics_path = REPO / "results" / exp / "metrics_test.json"
        if row["macro_f1"] is None:
            # Allowed: missing file or explicit null metrics
            if metrics_path.exists():
                payload = json.loads(metrics_path.read_text(encoding="utf-8"))
                assert payload.get("metrics", {}).get("macro_f1") is None
            continue
        assert metrics_path.exists(), f"Public macro_f1 set but missing {metrics_path}"
        payload = json.loads(metrics_path.read_text(encoding="utf-8"))
        assert payload["metrics"]["macro_f1"] == row["macro_f1"]


def test_no_fake_gemma_scores_without_predictions():
    for exp in ("gemma_zero_shot", "gemma_few_shot", "gemma_qlora"):
        metrics_path = REPO / "results" / exp / "metrics_test.json"
        if not metrics_path.exists():
            continue
        payload = json.loads(metrics_path.read_text(encoding="utf-8"))
        mf1 = payload.get("metrics", {}).get("macro_f1")
        pred = REPO / "results" / exp / "predictions_test.jsonl"
        if mf1 is not None:
            assert pred.exists(), f"{exp} has scores but no predictions"
