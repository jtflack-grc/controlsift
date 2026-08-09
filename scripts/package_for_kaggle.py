#!/usr/bin/env python3
"""Create a secret-safe zip for Kaggle Dataset upload.

Excludes credentials, venvs, git metadata, large weight blobs, and local caches.
Never pack .env or token files.
"""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

INCLUDE_PREFIXES = (
    "src/",
    "scripts/",
    "configs/",
    "data/processed/",
    "data/scenarios/",
    "data/manifests/",
    "notebooks/",
    "governance/PROTOCOL",
    "governance/RESEARCH_SURFACE.md",
    "governance/HUMAN_REVIEW.md",
    "governance/DATA_CARD.md",
    "governance/LIMITATIONS.md",
    "pyproject.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "README.md",
    "AGENTS.md",
    "LICENSE",
    "VERSION",
)

EXCLUDE_NAME_PARTS = (
    ".env",
    "hf_token",
    "kaggle.json",
    "credentials",
    "__pycache__",
    ".venv",
    "venv",
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".ipynb_checkpoints",
    ".safetensors",
    ".bin",
    "adapters/",
    "checkpoints/",
)


def _allowed(rel: str) -> bool:
    rel_posix = rel.replace("\\", "/")
    lower = rel_posix.lower()
    if any(part in lower for part in EXCLUDE_NAME_PARTS):
        return False
    if rel_posix in {
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
        "README.md",
        "AGENTS.md",
        "LICENSE",
    }:
        return True
    return any(rel_posix.startswith(prefix) for prefix in INCLUDE_PREFIXES)


def build_zip(out_path: Path) -> list[str]:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in REPO_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
            if not _allowed(rel):
                continue
            zf.write(path, arcname=f"controlsift/{rel}")
            written.append(rel)
    return written


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "dist" / "controlsift_kaggle_bundle.zip",
    )
    args = parser.parse_args()
    files = build_zip(args.out)
    print(f"Wrote {args.out} ({len(files)} files)")
    print("Review the zip before upload. It must not contain tokens or .env files.")


if __name__ == "__main__":
    main()
