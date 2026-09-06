#!/usr/bin/env python3
import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "notebooks" / "kaggle_runner.ipynb"
nb = json.loads(p.read_text(encoding="utf-8"))
url = "https://github.com/jtflack-grc/controlsift.git"

for cell in nb["cells"]:
    if cell.get("cell_type") != "code":
        continue
    src = "".join(cell.get("source", []))
    if "REPO_URL" in src and "SMOKE" in src:
        cell["source"] = [
            "# === Config (safe defaults) ===\n",
            "from pathlib import Path\n",
            "import os\n",
            "\n",
            "SMOKE = True          # True = short validation run; False = full test/challenge + train\n",
            "SMOKE_LIMIT = 16\n",
            f'REPO_URL = "{url}"\n',
            'REPO_BRANCH = "kaggle-bundle"\n',
            'KAGGLE_DATASET_DIR = "/kaggle/input"\n',
            "\n",
            'IN_COLAB = Path("/content").exists() and not Path("/kaggle").exists()\n',
            'WORKDIR = "/content/controlsift" if IN_COLAB else "/kaggle/working/controlsift"\n',
            "\n",
            'print("SMOKE =", SMOKE)\n',
            'print("IN_COLAB =", IN_COLAB)\n',
            'print("REPO_URL =", REPO_URL, "branch", REPO_BRANCH)\n',
            'print("WORKDIR =", WORKDIR)\n',
        ]
        break

for cell in nb["cells"]:
    if cell.get("cell_type") != "code":
        continue
    src = "".join(cell.get("source", []))
    if "Locate or fetch repo" not in src:
        continue
    cell["source"] = [
        line.replace(
            "!git clone --depth 1 {REPO_URL} {work}",
            "!git clone --depth 1 --branch {REPO_BRANCH} {REPO_URL} {work}",
        )
        for line in cell["source"]
    ]
    break

p.write_text(json.dumps(nb, indent=2) + "\n", encoding="utf-8")
print("wired", p)
