#!/usr/bin/env python3
"""Pin Kaggle runner to a single GPU before CUDA init."""
from __future__ import annotations

import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "notebooks" / "kaggle_runner.ipynb"
nb = json.loads(p.read_text(encoding="utf-8"))

for cell in nb["cells"]:
    if cell.get("cell_type") != "code":
        continue
    src = "".join(cell.get("source", []))
    if "SMOKE = True" not in src or "REPO_URL" not in src:
        continue
    cell["source"] = [
        "# === Config (safe defaults) ===\n",
        "from pathlib import Path\n",
        "import os\n",
        "\n",
        "# Kaggle T4x2: pin one GPU before any torch/CUDA import in later cells.\n",
        'os.environ["CUDA_VISIBLE_DEVICES"] = "0"\n',
        "\n",
        "SMOKE = True          # True = short validation run; False = full test/challenge + train\n",
        "SMOKE_LIMIT = 16\n",
        'REPO_URL = "https://github.com/jtflack-grc/controlsift.git"\n',
        'REPO_BRANCH = "kaggle-bundle"\n',
        'KAGGLE_DATASET_DIR = "/kaggle/input"\n',
        "\n",
        'IN_COLAB = Path("/content").exists() and not Path("/kaggle").exists()\n',
        'WORKDIR = "/content/controlsift" if IN_COLAB else "/kaggle/working/controlsift"\n',
        "\n",
        'print("SMOKE =", SMOKE)\n',
        'print("CUDA_VISIBLE_DEVICES =", os.environ.get("CUDA_VISIBLE_DEVICES"))\n',
        'print("IN_COLAB =", IN_COLAB)\n',
        'print("REPO_URL =", REPO_URL, "branch", REPO_BRANCH)\n',
        'print("WORKDIR =", WORKDIR)\n',
    ]
    break

p.write_text(json.dumps(nb, indent=2) + "\n", encoding="utf-8")
print("pinned single GPU in runner config")
