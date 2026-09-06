"""Patch kaggle_runner.ipynb for Colab auto-detect + zip upload bootstrap."""
from __future__ import annotations

import json
from pathlib import Path

p = Path("notebooks/kaggle_runner.ipynb")
nb = json.loads(p.read_text(encoding="utf-8"))

nb["cells"][0]["source"] = [
    "# ControlSift — Safe free GPU runner (Kaggle / Colab)\n",
    "\n",
    "**Security**\n",
    "- Put your Hugging Face token in platform secrets as `HF_TOKEN` only.\n",
    "- Never paste a token into a cell, chat, or committed file.\n",
    "- This notebook never prints the token.\n",
    "\n",
    "**Before you start**\n",
    "1. Accept the Gemma license on Hugging Face for `google/gemma-3-1b-it`.\n",
    "2. **Kaggle:** phone-verify account → Session options → Accelerator GPU · Secrets → `HF_TOKEN` · attach dataset zip.\n",
    "3. **Colab fallback** (if Kaggle GPU greyed out): Runtime → Change runtime type → GPU · Secrets → `HF_TOKEN` · upload `controlsift_kaggle_bundle.zip` in the bootstrap cell.\n",
    "\n",
    "Keep `SMOKE = True` for the first session.",
]

nb["cells"][1]["source"] = [
    "# === Config (safe defaults) ===\n",
    "from pathlib import Path\n",
    "\n",
    "SMOKE = True          # True = short validation run; False = full test/challenge + train\n",
    "SMOKE_LIMIT = 16\n",
    'REPO_URL = ""         # optional public clone URL (repo must contain data/processed)\n',
    'KAGGLE_DATASET_DIR = "/kaggle/input"\n',
    "\n",
    "# Auto-detect Colab vs Kaggle workdir\n",
    'IN_COLAB = Path("/content").exists() and not Path("/kaggle").exists()\n',
    'WORKDIR = "/content/controlsift" if IN_COLAB else "/kaggle/working/controlsift"\n',
    "\n",
    'print("SMOKE =", SMOKE)\n',
    'print("IN_COLAB =", IN_COLAB)\n',
    'print("WORKDIR =", WORKDIR)\n',
]

already = any(
    "Colab only: upload the local zip" in "".join(c.get("source", [])) for c in nb["cells"]
)
if not already:
    bootstrap = {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# === Colab only: upload the local zip (skip on Kaggle) ===\n",
            "from pathlib import Path\n",
            "import zipfile\n",
            "import shutil\n",
            "\n",
            "if IN_COLAB:\n",
            "    from google.colab import files\n",
            '    print("Upload dist/controlsift_kaggle_bundle.zip from your PC...")\n',
            "    uploaded = files.upload()\n",
            "    if not uploaded:\n",
            '        raise SystemExit("No file uploaded")\n',
            "    name = next(iter(uploaded))\n",
            '    dest = Path("/content") / name\n',
            '    extract_to = Path("/content/_bundle")\n',
            "    if extract_to.exists():\n",
            "        shutil.rmtree(extract_to)\n",
            "    extract_to.mkdir(parents=True)\n",
            '    with zipfile.ZipFile(dest, "r") as zf:\n',
            "        zf.extractall(extract_to)\n",
            "    candidates = list(extract_to.rglob(\"pyproject.toml\"))\n",
            "    if not candidates:\n",
            '        raise SystemExit("Zip missing pyproject.toml")\n',
            "    src = candidates[0].parent\n",
            "    work = Path(WORKDIR)\n",
            "    if work.exists():\n",
            "        shutil.rmtree(work)\n",
            "    shutil.copytree(src, work)\n",
            '    print("Colab bundle ready at", work)\n',
            "else:\n",
            '    print("Kaggle session — use attached Dataset (next cell).")\n',
        ],
    }
    nb["cells"].insert(2, bootstrap)

p.write_text(json.dumps(nb, indent=2) + "\n", encoding="utf-8")
print("updated", p, "cells", len(nb["cells"]))
