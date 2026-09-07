#!/usr/bin/env python3
"""Rebuild docs/data/failure_lab.json from TF-IDF confusions + published model preds."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]

MODEL_SPECS = (
    ("tfidf", "Classical baseline"),
    ("gemma_zero_shot", "Gemma 3 1B zero-shot"),
    ("gemma_few_shot", "Gemma 3 1B few-shot"),
    ("gemma_qlora", "Gemma 3 1B QLoRA"),
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def load_pred_rows(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    out: dict[str, dict[str, Any]] = {}
    if path.suffix == ".jsonl":
        rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    else:
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = payload["predictions"] if isinstance(payload, dict) and "predictions" in payload else payload
    for r in rows:
        cid = r.get("id") or r.get("case_id")
        if cid:
            out[cid] = r
    return out


def load_preds(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for cid, row in load_pred_rows(path).items():
        pred = row.get("pred_label") or row.get("prediction") or row.get("label")
        if pred:
            out[cid] = str(pred)
    return out


def pred_note(model: str, row: dict[str, Any] | None, fallback: str) -> str:
    if not row:
        return "Prediction file missing for this case"
    pred = row.get("pred_label")
    parse_status = row.get("parse_status")
    if pred is None:
        return "No pred_label in published run"
    if model == "tfidf":
        return fallback
    if parse_status == "unparseable" or pred == "UNPARSEABLE":
        return f"{fallback} · parse_status=unparseable"
    if parse_status:
        return f"{fallback} · parse_status={parse_status}"
    return fallback


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

    pred_maps = {
        name: load_pred_rows(REPO_ROOT / "results" / name / "predictions_test.jsonl")
        for name, _ in MODEL_SPECS
    }
    # Challenge fill cases may only exist in challenge predictions
    for name, _ in MODEL_SPECS:
        chal = load_pred_rows(REPO_ROOT / "results" / name / "predictions_challenge.jsonl")
        for cid, row in chal.items():
            pred_maps[name].setdefault(cid, row)

    tfidf_labels = {
        cid: (row.get("pred_label") or row.get("prediction") or row.get("label"))
        for cid, row in pred_maps["tfidf"].items()
    }

    selected: list[tuple[dict[str, Any], str | None]] = []
    mistakes_by_label: dict[str, list[str]] = {}
    for cid, case in test.items():
        pred = tfidf_labels.get(cid)
        if pred and pred != case["label"]:
            mistakes_by_label.setdefault(case["label"], []).append(cid)
    for label in sorted(mistakes_by_label):
        for cid in sorted(mistakes_by_label[label])[:2]:
            case = test[cid]
            selected.append((case, tfidf_labels.get(cid)))

    hard_tags = {"wrong_system", "evidence_not_traceable", "population_gap", "control_failure"}
    for case in sorted(challenge.values(), key=lambda c: c["id"]):
        if len(selected) >= 12:
            break
        if set(case.get("failure_tags") or []) & hard_tags:
            if case["id"] not in {c["id"] for c, _ in selected}:
                selected.append((case, tfidf_labels.get(case["id"])))

    lab_cases = []
    for case, tfidf_pred in selected[:12]:
        predictions = []
        for name, default_note in MODEL_SPECS:
            row = pred_maps[name].get(case["id"])
            pred = None
            if row:
                pred = row.get("pred_label") or row.get("prediction") or row.get("label")
            predictions.append(
                {
                    "model": name,
                    "pred_label": pred,
                    "note": pred_note(name, row, default_note),
                }
            )
        lab_cases.append(
            {
                "id": case["id"],
                "control_statement": case["control_statement"],
                "environment": case["environment"],
                "evidence_type": case["evidence_type"],
                "evidence_text": case["evidence_text"],
                "label": case["label"],
                "failure_tags": case.get("failure_tags") or [],
                "why_hard": why_hard(case, tfidf_pred),
                "predictions": predictions,
            }
        )

    payload = {
        "version": "1.1.0",
        "notes": (
            "Rebuilt from TF-IDF test confusions after v1.1 compositional hardening. "
            "Gemma zero-shot / few-shot / QLoRA predictions come from results/*/predictions_*.jsonl."
        ),
        "cases": lab_cases,
    }
    out = REPO_ROOT / "docs" / "data" / "failure_lab.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "n_cases": len(lab_cases), "out": str(out)}, indent=2))


if __name__ == "__main__":
    main()
