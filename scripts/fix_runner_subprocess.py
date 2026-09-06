#!/usr/bin/env python3
"""Replace os.system + SystemExit in kaggle_runner with subprocess + RuntimeError."""
from __future__ import annotations

import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "notebooks" / "kaggle_runner.ipynb"
nb = json.loads(p.read_text(encoding="utf-8"))

for cell in nb["cells"]:
    if cell.get("cell_type") != "code":
        continue
    src = "".join(cell.get("source", []))

    if "Gemma baselines" in src:
        cell["source"] = [
            "# === Gemma baselines ===\n",
            "import subprocess\n",
            "import sys\n",
            "\n",
            'limit_flag = f"--limit {SMOKE_LIMIT}" if SMOKE else ""\n',
            'splits = ["validation"] if SMOKE else ["validation", "test", "challenge"]\n',
            "\n",
            'for mode in ["zero_shot", "few_shot"]:\n',
            "    for split in splits:\n",
            '        cmd = [\n',
            '            sys.executable,\n',
            '            "scripts/run_gemma_baseline.py",\n',
            '            "--mode",\n',
            "            mode,\n",
            '            "--split",\n',
            "            split,\n",
            "        ]\n",
            "        if SMOKE:\n",
            '            cmd.extend(["--limit", str(SMOKE_LIMIT)])\n',
            '        print("\\n>>", " ".join(cmd))\n',
            "        subprocess.run(cmd, check=True)\n",
        ]
    elif "QLoRA train" in src:
        cell["source"] = [
            "# === QLoRA train ===\n",
            "import subprocess\n",
            "import sys\n",
            "\n",
            "train_cmd = [\n",
            "    sys.executable,\n",
            '    "-m",\n',
            '    "controlsift.training.train",\n',
            "]\n",
            "if SMOKE:\n",
            '    train_cmd.append("--smoke")\n',
            'print(">>", " ".join(train_cmd))\n',
            "subprocess.run(train_cmd, check=True)\n",
        ]
    elif "QLoRA eval" in src:
        cell["source"] = [
            "# === QLoRA eval ===\n",
            "import subprocess\n",
            "import sys\n",
            "\n",
            'limit_flag = []\n',
            "if SMOKE:\n",
            '    limit_flag = ["--limit", str(SMOKE_LIMIT)]\n',
            'splits = ["validation"] if SMOKE else ["validation", "test", "challenge"]\n',
            "\n",
            "for split in splits:\n",
            "    cmd = [\n",
            "        sys.executable,\n",
            '        "scripts/run_gemma_qlora_eval.py",\n',
            '        "--split",\n',
            "        split,\n",
            "        *limit_flag,\n",
            "    ]\n",
            '    print("\\n>>", " ".join(cmd))\n',
            "    subprocess.run(cmd, check=True)\n",
        ]
    elif "Install GPU deps" in src:
        # keep install but use RuntimeError for no-GPU
        cell["source"] = [
            line.replace("raise SystemExit(", "raise RuntimeError(")
            for line in cell["source"]
        ]
    elif "Auth via platform secrets" in src:
        cell["source"] = [
            line.replace("raise SystemExit(", "raise RuntimeError(")
            for line in cell["source"]
        ]
    elif "Locate or fetch repo" in src:
        cell["source"] = [
            line.replace("raise SystemExit(", "raise RuntimeError(")
            for line in cell["source"]
        ]

p.write_text(json.dumps(nb, indent=2) + "\n", encoding="utf-8")
print("patched runner error handling")
