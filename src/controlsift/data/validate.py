"""Dataset validation and integrity checks (charter §19, Gate 1)."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Optional

from controlsift import LABELS
from controlsift.data.schema import SPLITS, EvidenceCase
from controlsift.data.split import detect_family_leakage

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROCESSED = REPO_ROOT / "data" / "processed"

FORBIDDEN_PATTERNS = [
    re.compile(r"carecentrix", re.I),
    re.compile(r"password\s*=\s*\S+", re.I),
    re.compile(r"api[_-]?key\s*[:=]", re.I),
    re.compile(r"-----BEGIN (RSA )?PRIVATE KEY-----"),
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    return rows


def load_all_splits(processed_dir: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for split in SPLITS:
        path = processed_dir / f"{split}.jsonl"
        if not path.exists():
            raise FileNotFoundError(f"Missing split file: {path}")
        for row in load_jsonl(path):
            if row.get("split") != split:
                raise ValueError(f"{path}: case {row.get('id')} split mismatch")
            cases.append(row)
    return cases


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def validate_dataset(
    processed_dir: Path = DEFAULT_PROCESSED,
    *,
    expect_balanced: bool = True,
    per_class: Optional[dict[str, int]] = None,
) -> dict[str, Any]:
    """Validate schema, balance, leakage, duplicates. Raises ValueError on failure."""
    cases = load_all_splits(processed_dir)
    errors: list[str] = []

    # Schema
    for row in cases:
        try:
            EvidenceCase.model_validate(row)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"schema {row.get('id')}: {exc}")

    # Unique ids
    ids = [c["id"] for c in cases]
    dup_ids = [i for i, n in Counter(ids).items() if n > 1]
    if dup_ids:
        errors.append(f"duplicate ids: {dup_ids[:5]}")

    # Family leakage
    leaked = detect_family_leakage(cases)
    if leaked:
        errors.append(f"scenario family leakage across splits: {leaked[:10]}")

    # Exact / normalized duplicates of evidence_text
    texts = [normalize_text(c["evidence_text"]) for c in cases]
    text_counts = Counter(texts)
    dup_texts = [t for t, n in text_counts.items() if n > 1]
    if dup_texts:
        errors.append(f"duplicate evidence_text count: {len(dup_texts)}")

    # Labels / splits
    label_counts = Counter(c["label"] for c in cases)
    for label in LABELS:
        if label not in label_counts:
            errors.append(f"missing label: {label}")

    split_label: dict[str, Counter[str]] = defaultdict(Counter)
    for c in cases:
        split_label[c["split"]][c["label"]] += 1

    defaults = {
        "train": 200,
        "validation": 40,
        "test": 40,
        "challenge": 20,
    }
    targets = per_class or defaults
    if expect_balanced:
        for split, per in targets.items():
            for label in LABELS:
                n = split_label[split][label]
                if n != per:
                    errors.append(f"balance {split}/{label}: expected {per}, got {n}")

    # Forbidden patterns
    for c in cases:
        blob = " ".join(
            [
                c.get("evidence_text", ""),
                c.get("control_statement", ""),
                c.get("notes") or "",
            ]
        )
        for pat in FORBIDDEN_PATTERNS:
            if pat.search(blob):
                errors.append(f"forbidden pattern in {c['id']}: {pat.pattern}")

    # Domains coverage
    domains = {c["control_domain"] for c in cases}
    if len(domains) < 10:
        errors.append(f"expected ≥10 control domains, got {len(domains)}: {sorted(domains)}")

    report = {
        "ok": not errors,
        "total_cases": len(cases),
        "label_counts": dict(label_counts),
        "split_counts": dict(Counter(c["split"] for c in cases)),
        "n_domains": len(domains),
        "domains": sorted(domains),
        "n_families": len({c["scenario_family_id"] for c in cases}),
        "errors": errors,
    }
    if errors:
        raise ValueError("Dataset validation failed:\n- " + "\n- ".join(errors))
    return report


def main_cli(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Validate ControlSift dataset integrity")
    parser.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    parser.add_argument("--no-balance-check", action="store_true")
    args = parser.parse_args(argv)
    report = validate_dataset(
        args.processed,
        expect_balanced=not args.no_balance_check,
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main_cli()
