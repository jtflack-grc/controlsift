#!/usr/bin/env python3
"""Always re-clone kaggle-bundle so fixes are picked up on Run All."""
from __future__ import annotations

import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "notebooks" / "kaggle_runner.ipynb"
nb = json.loads(p.read_text(encoding="utf-8"))

for cell in nb["cells"]:
    if cell.get("cell_type") != "code":
        continue
    src = "".join(cell.get("source", []))
    if "Locate or fetch repo" not in src:
        continue
    cell["source"] = [
        "# === Locate or fetch repo (no secrets) ===\n",
        "import os\n",
        "import shutil\n",
        "import zipfile\n",
        "from pathlib import Path\n",
        "\n",
        "work = Path(WORKDIR)\n",
        "work.parent.mkdir(parents=True, exist_ok=True)\n",
        "\n",
        "def find_bundled_repo(root: Path) -> Path | None:\n",
        "    if not root.exists():\n",
        "        return None\n",
        "    for candidate in root.rglob(\"pyproject.toml\"):\n",
        "        text = candidate.read_text(encoding=\"utf-8\", errors=\"ignore\")\n",
        "        if 'name = \"controlsift\"' in text or \"name = 'controlsift'\" in text:\n",
        "            return candidate.parent\n",
        "    return None\n",
        "\n",
        "def extract_input_zips(root: Path) -> None:\n",
        "    if not root.exists():\n",
        "        return\n",
        "    for zpath in root.rglob(\"*.zip\"):\n",
        "        dest = Path(\"/kaggle/working\") / \"_extracted_dataset\" / zpath.stem\n",
        "        if (dest / \"controlsift\" / \"pyproject.toml\").exists() or (dest / \"pyproject.toml\").exists():\n",
        "            continue\n",
        "        dest.mkdir(parents=True, exist_ok=True)\n",
        "        print(\"Extracting\", zpath, \"→\", dest)\n",
        "        with zipfile.ZipFile(zpath, \"r\") as zf:\n",
        "            zf.extractall(dest)\n",
        "\n",
        "# Prefer a fresh clone when REPO_URL is set so GitHub fixes land without manual rm.\n",
        "if REPO_URL:\n",
        "    if work.exists():\n",
        "        shutil.rmtree(work)\n",
        "    !git clone --depth 1 --branch {REPO_BRANCH} {REPO_URL} {work}\n",
        "    print(\"Cloned\", REPO_URL, \"@\", REPO_BRANCH)\n",
        "else:\n",
        "    extract_input_zips(Path(KAGGLE_DATASET_DIR))\n",
        "    src = find_bundled_repo(Path(KAGGLE_DATASET_DIR))\n",
        "    if src is None:\n",
        "        src = find_bundled_repo(Path(\"/kaggle/working/_extracted_dataset\"))\n",
        "    if src is not None:\n",
        "        if work.exists():\n",
        "            shutil.rmtree(work)\n",
        "        shutil.copytree(src, work)\n",
        "        print(\"Copied dataset bundle from\", src)\n",
        "    elif Path(\"/content/controlsift\").exists():\n",
        "        work = Path(\"/content/controlsift\")\n",
        "        print(\"Using existing /content/controlsift\")\n",
        "    else:\n",
        "        raise RuntimeError(\n",
        "            \"Could not find ControlSift. Set REPO_URL or attach the Dataset zip.\"\n",
        "        )\n",
        "\n",
        "os.chdir(work)\n",
        "print(\"WORKDIR =\", work.resolve())\n",
        "assert (work / \"data\" / \"processed\" / \"train.jsonl\").exists(), \"missing train.jsonl\"\n",
        "assert (work / \"scripts\" / \"run_gemma_baseline.py\").exists(), \"missing scripts\"\n",
        "print(\"Input tree OK\")\n",
    ]
    break

p.write_text(json.dumps(nb, indent=2) + "\n", encoding="utf-8")
print("locate cell now always re-clones when REPO_URL set")
