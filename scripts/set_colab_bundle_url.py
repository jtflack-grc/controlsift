#!/usr/bin/env python3
"""Point Colab bootstrap at the published GitHub Release zip."""
from __future__ import annotations

import json
from pathlib import Path

BUNDLE_URL = (
    "https://github.com/jtflack-grc/controlsift/releases/download/"
    "kaggle-bundle/controlsift_kaggle_bundle.zip"
)

p = Path(__file__).resolve().parents[1] / "notebooks" / "kaggle_runner.ipynb"
nb = json.loads(p.read_text(encoding="utf-8"))

for cell in nb["cells"]:
    if cell.get("cell_type") != "code":
        continue
    src = "".join(cell.get("source", []))
    if "Colab only: upload" not in src:
        continue
    cell["source"] = [
        "# === Colab only: fetch or upload the bundle (skip on Kaggle) ===\n",
        "from pathlib import Path\n",
        "import zipfile\n",
        "import shutil\n",
        "import urllib.request\n",
        "\n",
        f'BUNDLE_URL = "{BUNDLE_URL}"\n',
        "\n",
        "if IN_COLAB:\n",
        "    dest = Path(\"/content/controlsift_kaggle_bundle.zip\")\n",
        "    extract_to = Path(\"/content/_bundle\")\n",
        "    try:\n",
        "        print(\"Downloading bundle from GitHub Release…\")\n",
        "        urllib.request.urlretrieve(BUNDLE_URL, dest)\n",
        "        print(\"Downloaded\", dest, \"bytes\", dest.stat().st_size)\n",
        "    except Exception as exc:\n",
        "        print(\"Release download failed:\", type(exc).__name__, exc)\n",
        "        from google.colab import files\n",
        "        print(\"Upload dist/controlsift_kaggle_bundle.zip from your PC…\")\n",
        "        uploaded = files.upload()\n",
        "        if not uploaded:\n",
        "            raise SystemExit(\"No bundle available\")\n",
        "        name = next(iter(uploaded))\n",
        "        dest = Path(\"/content\") / name\n",
        "    if extract_to.exists():\n",
        "        shutil.rmtree(extract_to)\n",
        "    extract_to.mkdir(parents=True)\n",
        "    with zipfile.ZipFile(dest, \"r\") as zf:\n",
        "        zf.extractall(extract_to)\n",
        "    candidates = list(extract_to.rglob(\"pyproject.toml\"))\n",
        "    if not candidates:\n",
        "        raise SystemExit(\"Zip missing pyproject.toml\")\n",
        "    src = candidates[0].parent\n",
        "    work = Path(WORKDIR)\n",
        "    if work.exists():\n",
        "        shutil.rmtree(work)\n",
        "    shutil.copytree(src, work)\n",
        "    print(\"Colab bundle ready at\", work)\n",
        "else:\n",
        "    print(\"Kaggle session — use attached Dataset (next cell).\")\n",
    ]
    break

# Refresh intro markdown Colab bullet
for cell in nb["cells"]:
    if cell.get("cell_type") != "markdown":
        continue
    src = "".join(cell.get("source", []))
    if "Safe free GPU runner" not in src:
        continue
    cell["source"] = [
        "# ControlSift — Safe free GPU runner (Kaggle / Colab)\n",
        "\n",
        "**Security**\n",
        "- Put your Hugging Face token in platform secrets as `HF_TOKEN` only.\n",
        "- Never paste a token into a cell, chat, or committed file.\n",
        "- This notebook never prints the token.\n",
        "\n",
        "**Before you start**\n",
        "1. Accept the Gemma license on Hugging Face for `google/gemma-3-1b-it`.\n",
        "2. **Kaggle:** phone-verify → Session options → GPU · Secrets → `HF_TOKEN` · attach dataset.\n",
        "3. **Colab fallback:** Runtime → GPU · run bootstrap (auto-downloads the GitHub Release zip) · Secrets/`getpass` for `HF_TOKEN`.\n",
        "\n",
        "Keep `SMOKE = True` for the first session.",
    ]
    break

p.write_text(json.dumps(nb, indent=2) + "\n", encoding="utf-8")
print("updated bootstrap →", BUNDLE_URL)
