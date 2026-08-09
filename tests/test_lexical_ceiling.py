"""Gate-1 integrity: committed benchmark must not be lexically trivial."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def _load(name: str) -> list[dict]:
    path = PROCESSED / f"{name}.jsonl"
    if not path.exists():
        pytest.skip("processed splits not present")
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _text(c: dict) -> str:
    return "\n".join([c["control_statement"], c["evidence_type"], c["evidence_text"]])


def test_tfidf_macro_f1_below_trivial_ceiling():
    train, test = _load("train"), _load("test")
    pipe = Pipeline(
        [
            ("tfidf", TfidfVectorizer(max_features=20000, ngram_range=(1, 2), min_df=2)),
            ("lr", LogisticRegression(max_iter=2000, class_weight="balanced", C=1.0, random_state=42)),
        ]
    )
    pipe.fit([_text(c) for c in train], [c["label"] for c in train])
    pred = pipe.predict([_text(c) for c in test])
    macro = f1_score([c["label"] for c in test], pred, average="macro")
    # Uncomfortable but above chance: reject both saturation and collapse.
    assert macro < 0.80, f"TF-IDF too strong (macro_f1={macro:.3f}); lexical shortcuts likely"
    assert macro > 0.25, f"TF-IDF unexpectedly weak (macro_f1={macro:.3f})"


def test_review_log_covers_full_challenge():
    import csv

    review = ROOT / "data" / "review_log.csv"
    if not review.exists():
        pytest.skip("review log missing")
    rows = list(csv.DictReader(review.open(encoding="utf-8")))
    challenge_ids = {c["id"] for c in _load("challenge")}
    logged = {r["id"] for r in rows if r.get("priority") == "challenge_required"}
    assert challenge_ids <= logged
    statuses = {r["review_status"] for r in rows if r["id"] in challenge_ids}
    assert "unreviewed" not in statuses
