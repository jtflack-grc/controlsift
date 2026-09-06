#!/usr/bin/env python3
"""Ensure Kaggle install cell pins transformers>=4.50 for Gemma 3."""
from __future__ import annotations

import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "notebooks" / "kaggle_runner.ipynb"
nb = json.loads(p.read_text(encoding="utf-8"))

for cell in nb["cells"]:
    if cell.get("cell_type") != "code":
        continue
    src = "".join(cell.get("source", []))
    if "Install GPU deps" not in src:
        continue
    cell["source"] = [
        "# === Install GPU deps + package ===\n",
        "import torch\n",
        "print(\"CUDA available:\", torch.cuda.is_available())\n",
        "if torch.cuda.is_available():\n",
        "    print(\"GPU:\", torch.cuda.get_device_name(0))\n",
        "else:\n",
        "    raise SystemExit(\n",
        "        \"No GPU visible. Session options → Accelerator → GPU T4, then Restart session.\"\n",
        "    )\n",
        "\n",
        "!pip -q install -U pip\n",
        '# Gemma 3 needs transformers>=4.50 (Kaggle images may ship older)\n',
        '!pip -q install -U "transformers>=4.50"\n',
        '!pip -q install -e ".[gpu]"\n',
        "import transformers\n",
        "print(\"transformers\", transformers.__version__)\n",
        "print(\"Install complete\")\n",
    ]
    break

p.write_text(json.dumps(nb, indent=2) + "\n", encoding="utf-8")
print("pinned transformers>=4.50 in", p)
