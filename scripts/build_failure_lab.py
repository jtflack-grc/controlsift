#!/usr/bin/env python3
"""Rebuild docs/data/failure_lab.json from TF-IDF confusions + challenge hard tags."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def load_preds(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    out: dict[str, str] = {}
    if path.suffix == ".jsonl":
        rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    else:
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = payload["predictions"] if isinstance(payload, dict) and "predictions" in payload else payload
    for r in rows:
        cid = r.get("id") or r.get("case_id")
        pred = r.get("pred_label") or r.get("prediction") or r.get("label")
        if cid and pred:
            out[cid] = pred
    return out


def why_hard(case: dict[str, Any], pred: str | None) -> str:
    label = case["label"]
    tags = ", ".join(case.get("failure_tags") or []) or "none"
    if pred and pred != label:
        return (
            f"TF-IDF predicted {pred} vs gold {label}. "
            f"Inspect SCOPE integers, Substance section pointer, and ROW_DETAIL. Tags: {tags}."
        )
    return (
        f"Challenge/hard case with gold {label}. "
        f"Compositional packet packing denies lexical shortcuts. Tags: {tags}."
    )


def main() -> None:
    processed = REPO_ROOT / "data" / "processed"
    test = {c["id"]: c for c in load_jsonl(processed / "test.jsonl")}
    challenge = {c["id"]: c for c in load_jsonl(processed / "challenge.jsonl")}
    preds = load_preds(REPO_ROOT / "results" / "tfidf" / "predictions_test.jsonl")

    selected: list[dict[str, Any]] = []
    # Prefer TF-IDF mistakes, stratified by gold label
    mistakes_by_label: dict[str, list[str]] = {}
    for cid, case in test.items():
        pred = preds.get(cid)
        if pred and pred != case["label"]:
            mistakes_by_label.setdefault(case["label"], []).append(cid)
    for label in sorted(mistakes_by_label):
        for cid in sorted(mistakes_by_label[label])[:2]:
            case = test[cid]
            selected.append((case, preds.get(cid)))

    # Fill with challenge hard tags
    hard_tags = {"wrong_system", "evidence_not_traceable", "population_gap", "control_failure"}
    for case in sorted(challenge.values(), key=lambda c: c["id"]):
        if len(selected) >= 12:
            break
        if set(case.get("failure_tags") or []) & hard_tags:
            if case["id"] not in {c["id"] for c, _ in selected}:
                selected.append((case, None))

    lab_cases = []
    for case, pred in selected[:12]:
        lab_cases.append(
            {
                "id": case["id"],
                "control_statement": case["control_statement"],
                "environment": case["environment"],
                "evidence_type": case["evidence_type"],
                "evidence_text": case["evidence_text"],
                "label": case["label"],
                "failure_tags": case.get("failure_tags") or [],
                "why_hard": why_hard(case, pred),
                "predictions": [
                    {
                        "model": "tfidf",
                        "pred_label": pred,
                        "note": "Classical baseline" if pred else "Not scored / challenge fill",
                    },
                    {
                        "model": "gemma_zero_shot",
                        "pred_label": None,
                        "note": "Pending GPU run",
                    },
                    {
                        "model": "gemma_qlora",
                        "pred_label": None,
                        "note": "Pending GPU run",
                    },
                ],
            }
        )

    payload = {
        "version": "1.1.0",
        "notes": (
            "Rebuilt from TF-IDF test confusions after v1.1 compositional hardening. "
            "LLM predictions remain null until Kaggle/HF runs."
        ),
        "cases": lab_cases,
    }
    out = REPO_ROOT / "docs" / "data" / "failure_lab.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "n_cases": len(lab_cases), "out": str(out)}, indent=2))


if __name__ == "__main__":
    main()
