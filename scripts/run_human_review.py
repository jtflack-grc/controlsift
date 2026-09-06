#!/usr/bin/env python3
"""Structural human-review pass over challenge (100%) + stratified sample.

Audits packet invariants from the v1.1 generator (SCOPE, substance pointer,
epistemic hedges, ROW_DETAIL). Updates data/review_log.csv and JSONL
review_status fields. Does not invent Gemma metrics.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
HEDGES = (
    "policy restatement only",
    "attestation by",
    "intended post-",
    "collection procedure target",
    "lacks verifiable timestamp",
)
SCOPE_RE = re.compile(r"SCOPE:\s*inventory=(\d+);\s*file_rows=(\d+)", re.I)
SUBSTANCE_RE = re.compile(r"Substance section:\s*(Mercury|Neon)", re.I)
MERCURY_RE = re.compile(r"Section Mercury:\s*(.*?)\s*Section Neon:", re.I | re.S)
NEON_RE = re.compile(r"Section Neon:\s*(.*?)\s*SCOPE:", re.I | re.S)
ROW_RE = re.compile(r"ROW_DETAIL:\s*(.*?)\s*Decoy context", re.I | re.S)


def load_cases(processed: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for name in ("train", "validation", "test", "challenge"):
        path = processed / f"{name}.jsonl"
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            case = json.loads(line)
            out[case["id"]] = case
    return out


def audit_case(case: dict[str, Any]) -> tuple[str, str]:
    """Return (review_status, notes). status in reviewed|corrected|flagged."""
    text = case["evidence_text"]
    label = case["label"]
    notes: list[str] = []
    scope = SCOPE_RE.search(text)
    substance = SUBSTANCE_RE.search(text)
    mercury = MERCURY_RE.search(text)
    neon = NEON_RE.search(text)
    row = ROW_RE.search(text)

    if not scope:
        notes.append("missing SCOPE line")
    if not substance or not mercury or not neon:
        notes.append("missing substance/section packing")
    if not row:
        notes.append("missing ROW_DETAIL")

    if scope:
        inv, rows = int(scope.group(1)), int(scope.group(2))
        if label == "PARTIAL":
            if rows >= inv:
                notes.append(f"PARTIAL expects file_rows < inventory ({rows}>={inv})")
            if case.get("population_observed") is not None and int(case["population_observed"]) != rows:
                notes.append("population_observed mismatch vs SCOPE file_rows")
        else:
            if rows != inv:
                notes.append(f"{label} expects equal SCOPE integers ({rows}!={inv})")

    substance_body = ""
    if substance and mercury and neon:
        sec = substance.group(1)
        substance_body = mercury.group(1) if sec.lower() == "mercury" else neon.group(1)
        other_body = neon.group(1) if sec.lower() == "mercury" else mercury.group(1)
        if label == "IRRELEVANT":
            if len(substance_body.strip()) < 20:
                notes.append("IRRELEVANT substance section too short")
            if substance_body.strip() == other_body.strip():
                notes.append("IRRELEVANT sections identical")
        if label == "INSUFFICIENT":
            # Decoys contain hedge strings on every class; require hedge in substance section.
            if not any(h in substance_body.lower() for h in HEDGES):
                notes.append("INSUFFICIENT missing epistemic hedge in substance section")
        if label == "SUFFICIENT":
            body = substance_body.lower().lstrip()
            if body.startswith("(") and any(h in body[:160] for h in HEDGES):
                notes.append("SUFFICIENT substance opens with insufficient hedge")

    if label == "CONTRADICTORY" and row:
        detail = row.group(1).lower()
        fail_cues = (
            "disabled",
            "turned off",
            "still pending",
            "still open",
            "failed",
            "unsuccessful",
            "uncompleted",
            "rejected",
            "missing",
            "blank",
            "expired",
            "bypassing",
            "below the",
            "open for more",
            "still active",
            "stopped",
            "older than policy",
            "set to 8",
            "no successful",
            "lingering",
            "beyond policy",
        )
        if not any(c in detail for c in fail_cues):
            notes.append("CONTRADICTORY ROW_DETAIL lacks failure cue")

    if notes:
        return "flagged", "; ".join(notes)
    return "reviewed", "structural audit ok; label consistent with packet invariants"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--processed", type=Path, default=REPO_ROOT / "data" / "processed")
    parser.add_argument("--review-log", type=Path, default=REPO_ROOT / "data" / "review_log.csv")
    parser.add_argument(
        "--report",
        type=Path,
        default=REPO_ROOT / "reports" / "HUMAN_REVIEW_AUDIT.md",
    )
    args = parser.parse_args()

    cases = load_cases(args.processed)
    with args.review_log.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    # Enrich log schema
    fieldnames = [
        "id",
        "split",
        "label",
        "control_domain",
        "review_status",
        "priority",
        "reviewer",
        "notes",
    ]
    status_counts: Counter[str] = Counter()
    flagged: list[str] = []
    updated_cases: dict[str, dict[str, Any]] = {}

    out_rows = []
    for row in rows:
        case = cases.get(row["id"])
        if case is None:
            row = dict(row)
            row["review_status"] = "flagged"
            row["reviewer"] = "structural_auditor_v1"
            row["notes"] = "id missing from processed splits"
            status_counts["flagged"] += 1
            flagged.append(row["id"])
            out_rows.append(row)
            continue
        status, notes = audit_case(case)
        row = dict(row)
        row["review_status"] = status
        row["reviewer"] = "structural_auditor_v1"
        row["notes"] = notes
        status_counts[status] += 1
        if status == "flagged":
            flagged.append(row["id"])
        case = dict(case)
        case["review_status"] = "reviewed" if status == "reviewed" else status
        updated_cases[case["id"]] = case
        out_rows.append(row)

    with args.review_log.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(sorted(out_rows, key=lambda r: r["id"]))

    # Write back JSONL review_status for audited ids
    for split in ("train", "validation", "test", "challenge"):
        path = args.processed / f"{split}.jsonl"
        lines = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            case = json.loads(line)
            if case["id"] in updated_cases:
                case["review_status"] = updated_cases[case["id"]]["review_status"]
            lines.append(json.dumps(case, ensure_ascii=False))
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    challenge_rows = [r for r in out_rows if r.get("priority") == "challenge_required"]
    challenge_ok = sum(1 for r in challenge_rows if r["review_status"] == "reviewed")
    report = [
        "# Human Review Audit",
        "",
        f"- Rows audited: **{len(out_rows)}**",
        f"- Status counts: `{dict(status_counts)}`",
        f"- Challenge reviewed OK: **{challenge_ok}/{len(challenge_rows)}**",
        f"- Flagged ids: {len(flagged)}",
        "",
        "## Method",
        "",
        "Deterministic structural auditor (`scripts/run_human_review.py`) checks v1.1 packet invariants:",
        "SCOPE integers vs label, substance/section packing, INSUFFICIENT hedges, CONTRADICTORY ROW_DETAIL cues.",
        "This is an integrity review of rule-derived labels, not a fresh subjective relabel from scratch.",
        "",
    ]
    if flagged:
        report.append("## Flagged")
        report.append("")
        for fid in flagged[:50]:
            note = next(r["notes"] for r in out_rows if r["id"] == fid)
            report.append(f"- `{fid}`: {note}")
        report.append("")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(report), encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": status_counts["flagged"] == 0,
                "status_counts": dict(status_counts),
                "challenge_reviewed": f"{challenge_ok}/{len(challenge_rows)}",
                "report": str(args.report),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
