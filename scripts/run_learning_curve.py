#!/usr/bin/env python3
"""Learning-curve experiment for TF-IDF (and placeholder hook for QLoRA subsets) §33."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from controlsift import CANONICAL_SEED, LABELS
from controlsift.evaluation.evaluate import load_jsonl
from controlsift.evaluation.metrics import compute_classification_metrics

REPO_ROOT = Path(__file__).resolve().parents[1]
SIZES = [100, 250, 500, 750, 1000]


def case_text(case: dict) -> str:
    return "\n".join(
        [case["control_statement"], case["evidence_type"], case["evidence_text"]]
    )


def stratified_subset(train: list[dict], n: int, seed: int = CANONICAL_SEED) -> list[dict]:
    per = max(1, n // len(LABELS))
    out: list[dict] = []
    for label in LABELS:
        pool = sorted([c for c in train if c["label"] == label], key=lambda c: c["id"])
        out.extend(pool[:per])
    return sorted(out, key=lambda c: c["id"])[:n]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=CANONICAL_SEED)
    args = parser.parse_args()

    train = load_jsonl(REPO_ROOT / "data" / "processed" / "train.jsonl")
    test = load_jsonl(REPO_ROOT / "data" / "processed" / "test.jsonl")
    curve = []
    for n in SIZES:
        subset = stratified_subset(train, n, seed=args.seed)
        pipe = Pipeline(
            [
                ("tfidf", TfidfVectorizer(max_features=20000, ngram_range=(1, 2), min_df=1)),
                (
                    "clf",
                    LogisticRegression(
                        max_iter=2000, class_weight="balanced", random_state=args.seed
                    ),
                ),
            ]
        )
        pipe.fit([case_text(c) for c in subset], [c["label"] for c in subset])
        preds = pipe.predict([case_text(c) for c in test])
        metrics = compute_classification_metrics([c["label"] for c in test], list(preds))
        curve.append({"n_train": len(subset), "macro_f1": metrics["macro_f1"]})

    out = {
        "experiment": "tfidf_learning_curve",
        "seed": args.seed,
        "split": "test",
        "points": curve,
        "notes": "QLoRA learning curve should be appended after GPU subset runs.",
    }
    path = REPO_ROOT / "results" / "tfidf" / "learning_curve.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
        f.write("\n")

    # Update learning-curve figure from real points
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot([p["n_train"] for p in curve], [p["macro_f1"] for p in curve], marker="o", color="#2f5d50")
    ax.set_ylim(0, 1)
    ax.set_xlabel("Training size")
    ax.set_ylabel("Test macro F1")
    ax.set_title("TF-IDF learning curve")
    fig.tight_layout()
    fig_path = REPO_ROOT / "reports" / "figures" / "05_learning_curve.png"
    fig.savefig(fig_path, dpi=150)
    plt.close(fig)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
