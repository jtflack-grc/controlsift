#!/usr/bin/env python3
"""Validate the Kaggle bundle before upload / after packaging."""
from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "dist" / "controlsift_kaggle_bundle.zip"
NEED = [
    "controlsift/pyproject.toml",
    "controlsift/notebooks/kaggle_runner.ipynb",
    "controlsift/data/processed/train.jsonl",
    "controlsift/data/processed/validation.jsonl",
    "controlsift/data/processed/test.jsonl",
    "controlsift/scripts/run_gemma_baseline.py",
    "controlsift/scripts/run_gemma_qlora_eval.py",
    "controlsift/configs/gemma3_1b_qlora.yaml",
]


def main() -> int:
    if not ZIP.is_file():
        print("MISSING", ZIP)
        return 1
    with zipfile.ZipFile(ZIP) as zf:
        names = set(zf.namelist())
        text = zf.read("controlsift/pyproject.toml").decode("utf-8", errors="ignore")
    ok = True
    for n in NEED:
        present = n in names
        print(("OK" if present else "MISSING"), n)
        ok = ok and present
    has_name = 'name = "controlsift"' in text or "name = 'controlsift'" in text
    print(("OK" if has_name else "MISSING"), "pyproject name=controlsift")
    ok = ok and has_name
    print("files", len(names), "bytes", ZIP.stat().st_size)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
