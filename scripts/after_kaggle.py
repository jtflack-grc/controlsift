#!/usr/bin/env python3
"""After a Kaggle/Colab download: refresh public metrics, figures, MMC comparative, docs sync.

Usage (repo root):
  python scripts/after_kaggle.py
  python scripts/after_kaggle.py --zip ~/Downloads/controlsift_gpu_outputs.zip

Does not invent metrics. Null Gemma rows stay null until result JSON files exist.
Never extracts secrets or large weight blobs from the zip.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_SUFFIXES = {".safetensors", ".bin", ".pt", ".pth", ".ckpt"}
ALLOWED_ROOT_PREFIXES = ("results/",)


def _run(args: list[str]) -> None:
    print("+", " ".join(args))
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def _metric_present(path: Path) -> bool:
    if not path.is_file():
        return False
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("metrics", {}).get("macro_f1") is not None


def _gemma_status() -> dict[str, dict[str, bool]]:
    out: dict[str, dict[str, bool]] = {}
    for name in ("gemma_zero_shot", "gemma_few_shot", "gemma_qlora"):
        base = ROOT / "results" / name
        out[name] = {
            "validation": _metric_present(base / "metrics_validation.json"),
            "test": _metric_present(base / "metrics_test.json"),
        }
    return out


def _safe_extract(zip_path: Path) -> list[str]:
    """Merge only results/** JSON-ish artifacts into the repo; skip weight shards."""
    if not zip_path.is_file():
        raise FileNotFoundError(f"Zip not found: {zip_path}")
    extracted: list[str] = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = info.filename.replace("\\", "/").lstrip("/")
            if name.startswith("../") or "/../" in name:
                print("SKIP unsafe path:", name)
                continue
            if not any(name.startswith(p) for p in ALLOWED_ROOT_PREFIXES):
                print("SKIP non-results path:", name)
                continue
            suffix = Path(name).suffix.lower()
            if suffix in SKIP_SUFFIXES:
                print("SKIP weight blob:", name)
                continue
            dest = ROOT / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(zf.read(info))
            extracted.append(name)
    print(json.dumps({"extracted_from_zip": len(extracted), "zip": str(zip_path)}, indent=2))
    for rel in extracted[:30]:
        print(" ", rel)
    if len(extracted) > 30:
        print(f"  ... +{len(extracted) - 30} more")
    return extracted


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--zip",
        type=Path,
        help="Path to controlsift_gpu_outputs.zip (optional; extracts results/ into repo)",
    )
    args = parser.parse_args()

    if args.zip is not None:
        _safe_extract(args.zip.resolve())

    status = _gemma_status()
    print(json.dumps({"gemma_metrics_present": status}, indent=2))
    any_val = any(v["validation"] for v in status.values())
    any_test = any(v["test"] for v in status.values())
    if not any_val and not any_test:
        print(
            "NOTE: No non-null Gemma metrics yet under results/gemma_*/.\n"
            "Pass --zip path/to/controlsift_gpu_outputs.zip after a Kaggle/Colab run."
        )
    elif any_val and not any_test:
        print(
            "NOTE: Smoke/validation metrics present, but public Results need test "
            "metrics. Re-run with SMOKE=False, download outputs, then "
            "re-run this script with --zip."
        )
    elif any_test:
        print("Test metrics present — public Results can leave pending.")

    _run(["scripts/run_evaluation.py"])
    _run(["scripts/build_figures.py"])
    _run(["-m", "mmc.labs.week11_comparative"])
    _run(["-m", "mmc.labs.sync_artifacts"])
    _run(["-m", "mmc.labs.build_week_pages"])
    print("Done. Check docs/results.html and docs/capstone/deliverables/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
