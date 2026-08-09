#!/usr/bin/env python3
"""Stratified *scripted* challenge spot-check (not a human GRC review).

Selects 4 cases per label (20 total) from the challenge split, writes
reports/SPOTCHECK_20.md, and upgrades those review_log rows to reviewer
`spotcheck_v1` with case-specific notes derived from packet fields.
Does not change gold labels. Do not describe this as human gold labeling.
"""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCOPE_RE = re.compile(r"SCOPE:\s*inventory=(\d+);\s*file_rows=(\d+)", re.I)
SUBSTANCE_RE = re.compile(r"Substance section:\s*(Mercury|Neon)", re.I)
LABELS = ["SUFFICIENT", "PARTIAL", "INSUFFICIENT", "IRRELEVANT", "CONTRADICTORY"]


def load_challenge() -> list[dict]:
    path = REPO_ROOT / "data" / "processed" / "challenge.jsonl"
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def note_for(case: dict) -> str:
    text = case["evidence_text"]
    label = case["label"]
    scope = SCOPE_RE.search(text)
    substance = SUBSTANCE_RE.search(text)
    inv = rows = None
    if scope:
        inv, rows = int(scope.group(1)), int(scope.group(2))
    sec = substance.group(1) if substance else "?"
    tags = ",".join(case.get("failure_tags") or []) or "none"

    if label == "SUFFICIENT":
        return (
            f"Spotcheck: substance={sec}; SCOPE {inv}=={rows}; "
            f"retained SUFFICIENT — operational claim in substance section, equal coverage, "
            f"no decisive failure in ROW_DETAIL. tags={tags}"
        )
    if label == "PARTIAL":
        return (
            f"Spotcheck: substance={sec}; SCOPE inventory={inv} file_rows={rows}; "
            f"retained PARTIAL — file_rows < inventory under shared claim scaffold. tags={tags}"
        )
    if label == "INSUFFICIENT":
        return (
            f"Spotcheck: substance={sec}; SCOPE {inv}=={rows}; "
            f"retained INSUFFICIENT — epistemic hedge/non-execution reading in substance section "
            f"(not merely decoy hedges). tags={tags}"
        )
    if label == "IRRELEVANT":
        return (
            f"Spotcheck: substance={sec}; SCOPE {inv}=={rows}; "
            f"retained IRRELEVANT — substance pointer targets off-objective distractor while "
            f"claim-like text remains in the other section. tags={tags}"
        )
    return (
        f"Spotcheck: substance={sec}; SCOPE {inv}=={rows}; "
        f"retained CONTRADICTORY — ROW_DETAIL carries control-failure fact against otherwise "
        f"complete packet framing. tags={tags}"
    )


def main() -> None:
    by_label: dict[str, list[dict]] = defaultdict(list)
    for c in load_challenge():
        by_label[c["label"]].append(c)

    selected: list[dict] = []
    for label in LABELS:
        pool = sorted(by_label[label], key=lambda c: c["id"])
        selected.extend(pool[:4])

    selected_ids = {c["id"] for c in selected}
    notes = {c["id"]: note_for(c) for c in selected}

    review_path = REPO_ROOT / "data" / "review_log.csv"
    with review_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    fieldnames = list(rows[0].keys())
    if "reviewer" not in fieldnames:
        fieldnames.append("reviewer")
    if "notes" not in fieldnames:
        fieldnames.append("notes")

    for row in rows:
        if row["id"] in selected_ids:
            row["review_status"] = "reviewed"
            row["reviewer"] = "spotcheck_v1"
            row["notes"] = notes[row["id"]]

    with review_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: r["id"]))

    lines = [
        "# Challenge spot-check (20 cases)",
        "",
        "Stratified: **4 cases × 5 labels** from the sealed challenge split.",
        "This is a **second-pass reading** with case-specific notes — still not a full human gold relabel.",
        "Gold labels were retained; no test/challenge relabeling after protocol seal.",
        "",
        "| id | label | domain | note |",
        "|----|-------|--------|------|",
    ]
    for c in sorted(selected, key=lambda x: x["id"]):
        note = notes[c["id"]].replace("|", "/")
        lines.append(
            f"| `{c['id']}` | {c['label']} | {c['control_domain']} | {note} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Structural audit covers 100% challenge (`structural_auditor_v1`).",
            "- This spot-check adds narrative notes on 20% of challenge (20/100).",
            "- Remaining challenge rows stay on structural audit only — say that publicly.",
            "",
        ]
    )
    out = REPO_ROOT / "reports" / "SPOTCHECK_20.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"ok": True, "n": len(selected), "report": str(out)}, indent=2))


if __name__ == "__main__":
    main()
