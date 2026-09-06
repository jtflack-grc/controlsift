#!/usr/bin/env python3
"""Write protocol seal artifact from current dataset manifest hashes."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    manifest_path = REPO_ROOT / "data" / "manifests" / "dataset_manifest.json"
    with manifest_path.open(encoding="utf-8") as f:
        manifest = json.load(f)

    seal = {
        "protocol_tag": "protocol-v1-locked",
        "sealed_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_version": manifest.get("dataset_version"),
        "seed": manifest.get("seed"),
        "primary_metric": "macro_f1",
        "model_id": "google/gemma-3-1b-it",
        "prompt_module": "src/controlsift/prompting/templates.py",
        "test_sha256": manifest["files"]["test"]["sha256"],
        "validation_sha256": manifest["files"]["validation"]["sha256"],
        "challenge_sha256": manifest["files"]["challenge"]["sha256"],
        "train_sha256": manifest["files"]["train"]["sha256"],
        "notes": (
            "Do not modify the canonical prompt or relabel the test set after this seal. "
            "Create git tag protocol-v1-locked when committing this file."
        ),
    }
    out = REPO_ROOT / "governance" / "PROTOCOL_SEAL.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(seal, f, indent=2)
        f.write("\n")
    print(json.dumps(seal, indent=2))


if __name__ == "__main__":
    main()
