"""Harden kaggle_runner post-locate cells: cwd + SMOKE defaults, clean install.

Applies to notebooks/kaggle_runner.ipynb in-place. Safe to re-run.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks" / "kaggle_runner.ipynb"

GUARD = '''# Ensure cwd + smoke flags even if cells are re-run out of order
import os
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
if "IN_COLAB" not in globals():
    IN_COLAB = Path("/content").exists() and not Path("/kaggle").exists()
if "WORKDIR" not in globals():
    WORKDIR = "/content/controlsift" if IN_COLAB else "/kaggle/working/controlsift"
if "SMOKE" not in globals():
    SMOKE = True
if "SMOKE_LIMIT" not in globals():
    SMOKE_LIMIT = 16
work = Path(WORKDIR)
if not work.exists():
    raise RuntimeError(f"WORKDIR missing ({work}). Re-run Locate first.")
os.chdir(work)
print("cwd =", Path.cwd())
print("SMOKE =", SMOKE, "SMOKE_LIMIT =", SMOKE_LIMIT)
'''

INSTALL = '''# === Install GPU deps + package ===
import os
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
if "IN_COLAB" not in globals():
    IN_COLAB = Path("/content").exists() and not Path("/kaggle").exists()
if "WORKDIR" not in globals():
    WORKDIR = "/content/controlsift" if IN_COLAB else "/kaggle/working/controlsift"
work = Path(WORKDIR)
if not work.exists():
    raise RuntimeError(f"WORKDIR missing ({work}). Re-run Locate first.")
os.chdir(work)
print("cwd =", Path.cwd())

import torch
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print("capability:", torch.cuda.get_device_capability(0))
else:
    raise RuntimeError(
        "No GPU visible. Session options → Accelerator → GPU T4, then Restart session."
    )

!pip -q install -U pip
# Gemma 3: transformers>=4.50; TRL: SFTConfig; peft: torchao>=0.16 if present.
!pip -q install -U "transformers>=4.50" "trl>=0.14" "torchao>=0.16"
!pip -q install -e ".[gpu]"
# peft>=0.16 raises if stale torchao remains — upgrade then uninstall fallback.
import subprocess, sys
def _torchao_ok() -> bool:
    try:
        import importlib.metadata as md
        ver = md.version("torchao")
    except Exception:
        print("torchao: not installed (ok)")
        return True
    parts = []
    for chunk in ver.split("."):
        digits = "".join(ch for ch in chunk if ch.isdigit())
        if not digits:
            break
        parts.append(int(digits))
        if len(parts) == 3:
            break
    while len(parts) < 3:
        parts.append(0)
    ok = tuple(parts) >= (0, 16, 0)
    print("torchao:", ver, ("ok" if ok else "TOO OLD"))
    return ok
if not _torchao_ok():
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "torchao>=0.16"], check=False)
if not _torchao_ok():
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "torchao"], check=False)
    print("Uninstalled torchao as fallback (peft only probes it)")
import transformers
import trl
print("transformers", transformers.__version__)
print("trl", trl.__version__)
print("Install complete")
'''

BASELINES = GUARD + '''
# === Gemma baselines ===
import subprocess
import sys

splits = ["validation"] if SMOKE else ["validation", "test", "challenge"]

for mode in ["zero_shot", "few_shot"]:
    for split in splits:
        cmd = [
            sys.executable,
            "scripts/run_gemma_baseline.py",
            "--mode",
            mode,
            "--split",
            split,
        ]
        if SMOKE:
            cmd.extend(["--limit", str(SMOKE_LIMIT)])
        print("\\n>>", " ".join(cmd))
        subprocess.run(cmd, check=True)
print("Baselines complete")
'''

TRAIN = GUARD + '''
# === QLoRA train ===
import subprocess
import sys

train_cmd = [
    sys.executable,
    "-m",
    "controlsift.training.train",
]
if SMOKE:
    train_cmd.append("--smoke")
print(">>", " ".join(train_cmd))
subprocess.run(train_cmd, check=True)
print("Train complete — expect precision print with fp16_amp: False on T4")
'''

EVAL = GUARD + '''
# === QLoRA eval ===
import subprocess
import sys
from pathlib import Path

adapter = Path("results/gemma_qlora/adapter")
if not adapter.exists():
    raise RuntimeError(
        f"Adapter missing at {adapter.resolve()}. Re-run train cell first."
    )

limit_flag = ["--limit", str(SMOKE_LIMIT)] if SMOKE else []
splits = ["validation"] if SMOKE else ["validation", "test", "challenge"]

for split in splits:
    cmd = [
        sys.executable,
        "scripts/run_gemma_qlora_eval.py",
        "--split",
        split,
        *limit_flag,
    ]
    print("\\n>>", " ".join(cmd))
    subprocess.run(cmd, check=True)
print("QLoRA eval complete")
'''

PACKAGE = GUARD + '''
# === Package downloadable outputs (metrics/preds/meta; skip huge weights by default) ===
import json
import zipfile
from pathlib import Path

INCLUDE_LARGE_ADAPTER = False  # set True only if you knowingly want a large zip

out_zip = Path("/kaggle/working/controlsift_gpu_outputs.zip")
if not out_zip.parent.exists():
    out_zip = Path("/content/controlsift_gpu_outputs.zip") if IN_COLAB else Path("controlsift_gpu_outputs.zip")

roots = [
    Path("results/gemma_zero_shot"),
    Path("results/gemma_few_shot"),
    Path("results/gemma_qlora"),
]

written = []
with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            rel = str(path).replace("\\\\", "/")
            if path.suffix in {".safetensors", ".bin", ".pt", ".pth"} and not INCLUDE_LARGE_ADAPTER:
                continue
            if "adapter/" in rel and path.suffix not in {".json", ".txt", ".md"} and not INCLUDE_LARGE_ADAPTER:
                # keep tokenizer/config json; skip weight shards
                if path.name.startswith("adapter_model") or path.name.startswith("model"):
                    continue
            zf.write(path, arcname=rel)
            written.append(rel)

print("Wrote", out_zip.resolve(), "files:", len(written))
print("Download this zip → unzip into your local repo root → run:")
print("  python scripts/after_kaggle.py --zip path/to/controlsift_gpu_outputs.zip")

def _macro(path: Path):
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("metrics", {}).get("macro_f1")
    except Exception:
        return None

status = {}
for exp in ("gemma_zero_shot", "gemma_few_shot", "gemma_qlora"):
    status[exp] = {
        "validation_macro_f1": _macro(Path("results") / exp / "metrics_validation.json"),
        "test_macro_f1": _macro(Path("results") / exp / "metrics_test.json"),
    }
print(json.dumps({"packaged_metrics": status, "SMOKE": SMOKE}, indent=2))
if SMOKE:
    print("NOTE: smoke writes validation only — set SMOKE=False for public test metrics")
'''


def _as_source(text: str) -> list[str]:
    # Notebook JSON stores lines with trailing newlines.
    if not text.endswith("\n"):
        text += "\n"
    return [line + "\n" for line in text.splitlines()]


def main() -> None:
    data = json.loads(NB.read_text(encoding="utf-8"))
    cells = data["cells"]
    assert "Install GPU deps" in "".join(cells[5]["source"])
    assert "Gemma baselines" in "".join(cells[6]["source"])
    assert "QLoRA train" in "".join(cells[7]["source"])
    assert "QLoRA eval" in "".join(cells[8]["source"])
    assert "Package downloadable" in "".join(cells[9]["source"])

    cells[5]["source"] = _as_source(INSTALL)
    cells[6]["source"] = _as_source(BASELINES)
    cells[7]["source"] = _as_source(TRAIN)
    cells[8]["source"] = _as_source(EVAL)
    cells[9]["source"] = _as_source(PACKAGE)

    NB.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Patched", NB)
    # sanity
    src9 = "".join(cells[9]["source"])
    assert "packaged_metrics" in src9
    assert "WORKDIR missing" in "".join(cells[6]["source"])
    print("OK")


if __name__ == "__main__":
    main()
