#!/usr/bin/env python3
"""Run majority + TF-IDF logistic regression baselines (§24)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from controlsift import CANONICAL_SEED
from controlsift.evaluation.evaluate import (
    evaluate_predictions,
    load_jsonl,
    save_predictions,
    write_json,
)
from controlsift.evaluation.metrics import empty_metrics_payload, majority_baseline_predictions

REPO_ROOT = Path(__file__).resolve().parents[1]


def case_text(case: dict) -> str:
    return "\n".join(
        [
            case["control_statement"],
            case["evidence_type"],
            case["evidence_text"],
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "configs" / "baseline.yaml")
    args = parser.parse_args()
    with args.config.open(encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    train = load_jsonl(REPO_ROOT / cfg["paths"]["train"])
    val = load_jsonl(REPO_ROOT / cfg["paths"]["validation"])
    test = load_jsonl(REPO_ROOT / cfg["paths"]["test"])
    challenge = load_jsonl(REPO_ROOT / cfg["paths"]["challenge"])

    seed = int(cfg.get("seed", CANONICAL_SEED))
    dataset_version = str(cfg.get("dataset_version", "1.0.0"))

    # --- Majority ---
    maj_dir = REPO_ROOT / "results" / "majority"
    for split_name, split_cases in [
        ("validation", val),
        ("test", test),
        ("challenge", challenge),
    ]:
        preds = majority_baseline_predictions(
            [c["label"] for c in train],
            len(split_cases),
        )
        pred_rows = [
            {"id": c["id"], "pred_label": p, "split": split_name}
            for c, p in zip(split_cases, preds)
        ]
        save_predictions(maj_dir / f"predictions_{split_name}.jsonl", pred_rows)
        payload = evaluate_predictions(
            split_cases,
            pred_rows,
            experiment="majority",
            dataset_version=dataset_version,
            model="majority_class",
            seed=seed,
            run_bootstrap=split_name == "test",
        )
        write_json(maj_dir / f"metrics_{split_name}.json", payload)

    # --- TF-IDF ---
    tfidf_cfg = cfg["model"]["tfidf"]
    lr_cfg = cfg["model"]["logistic_regression"]
    pipe = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=tfidf_cfg.get("max_features", 20000),
                    ngram_range=tuple(tfidf_cfg.get("ngram_range", [1, 2])),
                    min_df=tfidf_cfg.get("min_df", 2),
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    max_iter=lr_cfg.get("max_iter", 2000),
                    class_weight=lr_cfg.get("class_weight", "balanced"),
                    C=lr_cfg.get("C", 1.0),
                    random_state=seed,
                ),
            ),
        ]
    )
    pipe.fit([case_text(c) for c in train], [c["label"] for c in train])

    out_dir = REPO_ROOT / cfg["paths"]["output_dir"]
    summary = {}
    for split_name, split_cases in [
        ("validation", val),
        ("test", test),
        ("challenge", challenge),
    ]:
        pred_labels = pipe.predict([case_text(c) for c in split_cases])
        pred_rows = [
            {"id": c["id"], "pred_label": str(p), "split": split_name}
            for c, p in zip(split_cases, pred_labels)
        ]
        save_predictions(out_dir / f"predictions_{split_name}.jsonl", pred_rows)
        payload = evaluate_predictions(
            split_cases,
            pred_rows,
            experiment="tfidf",
            dataset_version=dataset_version,
            model="tfidf_logistic_regression",
            seed=seed,
            run_bootstrap=split_name == "test",
        )
        write_json(out_dir / f"metrics_{split_name}.json", payload)
        summary[split_name] = payload["metrics"]["macro_f1"]

    # Gate-1 note: lexical ceiling check
    note_path = out_dir / "gate1_lexical_note.json"
    write_json(
        note_path,
        {
            "warning_threshold_macro_f1": 0.95,
            "validation_macro_f1": summary.get("validation"),
            "test_macro_f1": summary.get("test"),
            "challenge_macro_f1": summary.get("challenge"),
            "interpretation": (
                "If TF-IDF macro F1 is extremely high on held-out splits, "
                "inspect for lexical shortcuts before protocol lock."
            ),
        },
    )

    # Ensure empty null payloads exist for LLM experiments until run
    for exp, model in [
        ("gemma_zero_shot", "google/gemma-3-1b-it"),
        ("gemma_few_shot", "google/gemma-3-1b-it"),
        ("gemma_qlora", "google/gemma-3-1b-it+qlora"),
    ]:
        path = REPO_ROOT / "results" / exp / "metrics_test.json"
        if not path.exists():
            write_json(
                path,
                empty_metrics_payload(exp, dataset_version=dataset_version, model=model, seed=seed),
            )

    print(json.dumps({"ok": True, "tfidf_macro_f1": summary}, indent=2))


if __name__ == "__main__":
    main()
