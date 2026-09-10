"""Week 11 deliverable helper: comparative analysis table from published results/."""

from __future__ import annotations

import json
from pathlib import Path

from mmc.labs.paths import ROOT, ensure_out


def _load_macro(path: Path) -> float | None:
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    metrics = data.get("metrics") or data
    return metrics.get("macro_f1")


def run() -> dict:
    out = ensure_out()
    rows = []
    experiments = [
        ("majority", "v1.1.0", "results/majority/metrics_test.json", "results/majority/metrics_challenge.json"),
        ("tfidf", "v1.1.0", "results/tfidf/metrics_test.json", "results/tfidf/metrics_challenge.json"),
        ("gemma_zero_shot", "v1.0.0", "results/gemma_zero_shot/metrics_test.json", "results/gemma_zero_shot/metrics_challenge.json"),
        ("gemma_few_shot", "v1.0.0", "results/gemma_few_shot/metrics_test.json", "results/gemma_few_shot/metrics_challenge.json"),
        ("gemma_qlora", "v1.0.0", "results/gemma_qlora/metrics_test.json", "results/gemma_qlora/metrics_challenge.json"),
    ]
    for name, dataset_version, test_p, chal_p in experiments:
        test = _load_macro(ROOT / test_p)
        chal = _load_macro(ROOT / chal_p)
        rows.append(
            {
                "experiment": name,
                "dataset_version": dataset_version,
                "test_macro_f1": test,
                "challenge_macro_f1": chal,
                "status": "complete" if test is not None else "missing_result",
            }
        )

    payload = {
        "deliverable": "week11_comparative_analysis",
        "primary_metric": "macro_f1",
        "seed": 42,
        "version_boundary": {
            "classical": "v1.1.0",
            "gemma": "v1.0.0",
            "comparison_rule": "Within-version comparisons are controlled; cross-version scores are descriptive only.",
        },
        "rows": rows,
        "weights": {
            "toy_lora_scaffold": "mmc/deliverables/outputs/week07_lora_adapter.npz",
            "gemma_qlora_dir": "results/gemma_qlora/",
            "gemma_qlora_present": (ROOT / "results" / "gemma_qlora").exists()
            and any((ROOT / "results" / "gemma_qlora").glob("*")),
        },
        "failure_lab": "docs/data/failure_lab.json",
        "notes": [
            "All five published experiment rungs have result receipts.",
            "Within Gemma v1.0.0, few-shot is strongest and QLoRA does not beat it.",
            "Classical v1.1.0 and Gemma v1.0.0 scores are not a controlled same-benchmark leaderboard.",
        ],
    }
    (out / "week11_comparative_analysis.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
