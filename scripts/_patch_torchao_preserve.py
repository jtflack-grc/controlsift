"""Patch kaggle_runner.ipynb: preserve results on Locate; torchao in Install."""

from __future__ import annotations

import json
from pathlib import Path

NB = Path(__file__).resolve().parents[1] / "notebooks" / "kaggle_runner.ipynb"

LOCATE = r'''# === Locate or fetch repo (no secrets) ===
# Every run with REPO_URL set: fresh-clone branch tip, print HEAD SHA.
# Preserves WORKDIR/results (and adapter) across reclone so smoke train survives refresh.
# Safe defaults if Config was not run in this kernel (NameError-proof).
import os
import shutil
import subprocess
import zipfile
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")

# Do not overwrite REPO_* / SMOKE if Config already set them.
if "REPO_URL" not in globals():
    REPO_URL = "https://github.com/jtflack-grc/controlsift.git"
if "REPO_BRANCH" not in globals():
    REPO_BRANCH = "kaggle-bundle"
if "KAGGLE_DATASET_DIR" not in globals():
    KAGGLE_DATASET_DIR = "/kaggle/input"
if "IN_COLAB" not in globals():
    IN_COLAB = Path("/content").exists() and not Path("/kaggle").exists()
if "WORKDIR" not in globals():
    WORKDIR = "/content/controlsift" if IN_COLAB else "/kaggle/working/controlsift"
if "SMOKE" not in globals():
    SMOKE = True
if "SMOKE_LIMIT" not in globals():
    SMOKE_LIMIT = 16

print(
    "Locate defaults:",
    {
        "IN_COLAB": IN_COLAB,
        "WORKDIR": WORKDIR,
        "REPO_URL": REPO_URL,
        "REPO_BRANCH": REPO_BRANCH,
        "SMOKE": SMOKE,
    },
)

work = Path(WORKDIR)
work.parent.mkdir(parents=True, exist_ok=True)

# Paths preserved across rmtree/reclone so QLoRA adapter + metrics survive code refresh.
PRESERVE_RELPATHS = ("results",)


def _stash_dir() -> Path:
    return work.parent / "_controlsift_preserve"


def stash_workdir_outputs(dest: Path) -> Path | None:
    """Copy results/ aside before deleting WORKDIR."""
    if not dest.exists():
        return None
    found = [dest / rel for rel in PRESERVE_RELPATHS if (dest / rel).exists()]
    if not found:
        print("No results/ to preserve (fresh session or train not run yet)")
        return None
    stash = _stash_dir()
    if stash.exists():
        shutil.rmtree(stash)
    stash.mkdir(parents=True)
    for src in found:
        target = stash / src.name
        shutil.copytree(src, target)
        print(f"Preserved {src} -> {target}")
    return stash


def restore_workdir_outputs(dest: Path, stash: Path | None) -> None:
    """Merge stashed results/ back after clone (stashed wins on conflicts)."""
    if stash is None or not stash.exists():
        return
    for item in stash.iterdir():
        target = dest / item.name
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)
        print(f"Restored preserved {item.name} -> {target}")
    shutil.rmtree(stash, ignore_errors=True)
    adapter = dest / "results" / "gemma_qlora" / "adapter"
    print("Adapter present after restore:", adapter.exists(), adapter)


def find_bundled_repo(root: Path) -> Path | None:
    if not root.exists():
        return None
    for candidate in root.rglob("pyproject.toml"):
        text = candidate.read_text(encoding="utf-8", errors="ignore")
        if 'name = "controlsift"' in text or "name = 'controlsift'" in text:
            return candidate.parent
    return None

def extract_input_zips(root: Path) -> None:
    if not root.exists():
        return
    for zpath in root.rglob("*.zip"):
        dest = Path("/kaggle/working") / "_extracted_dataset" / zpath.stem
        if (dest / "controlsift" / "pyproject.toml").exists() or (dest / "pyproject.toml").exists():
            continue
        dest.mkdir(parents=True, exist_ok=True)
        print("Extracting", zpath, "->", dest)
        with zipfile.ZipFile(zpath, "r") as zf:
            zf.extractall(dest)

def clone_repo(url: str, branch: str, dest: Path) -> str:
    """Fresh clone via subprocess (IPython !git does NOT raise on failure)."""
    if dest.exists():
        print("Removing existing", dest, "(results already stashed if present)")
        shutil.rmtree(dest)
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    cmd = [
        "git",
        "clone",
        "--depth",
        "1",
        "--branch",
        branch,
        url,
        str(dest),
    ]
    print(">>", " ".join(cmd))
    try:
        proc = subprocess.run(
            cmd,
            check=True,
            env=env,
            capture_output=True,
            text=True,
        )
        if proc.stdout:
            print(proc.stdout)
        if proc.stderr:
            print(proc.stderr)
    except FileNotFoundError as exc:
        raise RuntimeError(
            "git not found on PATH. On Kaggle, Internet must be ON and git available."
        ) from exc
    except subprocess.CalledProcessError as exc:
        print("STDOUT:", exc.stdout)
        print("STDERR:", exc.stderr)
        raise RuntimeError(
            f"git clone failed (exit {exc.returncode}). "
            "Session options -> turn Internet ON, confirm REPO_URL/REPO_BRANCH, re-run this cell."
        ) from exc
    if not dest.exists():
        raise RuntimeError(f"Clone reported OK but workdir missing: {dest}")
    sha = subprocess.check_output(
        ["git", "-C", str(dest), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    branch_out = subprocess.check_output(
        ["git", "-C", str(dest), "rev-parse", "--abbrev-ref", "HEAD"],
        text=True,
    ).strip()
    print(f"Cloned {url} branch={branch} HEAD={sha} (ref={branch_out})")
    return sha

# Prefer a fresh clone when REPO_URL is set so GitHub fixes land every locate run.
# Stash results/ first so a successful smoke train is not wiped.
preserved = stash_workdir_outputs(work)
try:
    if REPO_URL:
        clone_repo(REPO_URL, REPO_BRANCH, work)
    else:
        extract_input_zips(Path(KAGGLE_DATASET_DIR))
        src = find_bundled_repo(Path(KAGGLE_DATASET_DIR))
        if src is None:
            src = find_bundled_repo(Path("/kaggle/working/_extracted_dataset"))
        if src is not None:
            if work.exists():
                shutil.rmtree(work)
            shutil.copytree(src, work)
            print("Copied dataset bundle from", src)
        elif Path("/content/controlsift").exists():
            work = Path("/content/controlsift")
            print("Using existing /content/controlsift")
        else:
            raise RuntimeError(
                "Could not find ControlSift. Set REPO_URL or attach the Dataset zip."
            )
finally:
    restore_workdir_outputs(work, preserved)

if not work.exists():
    raise RuntimeError(f"WORKDIR missing after locate: {work}")

os.chdir(work)
print("WORKDIR =", work.resolve())
assert (work / "data" / "processed" / "train.jsonl").exists(), "missing train.jsonl"
assert (work / "scripts" / "run_gemma_baseline.py").exists(), "missing scripts"
print("Input tree OK")
'''

INSTALL = r'''# === Install GPU deps + package ===
import os
import subprocess
import sys
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
        "No GPU visible. Session options \u2192 Accelerator \u2192 GPU T4, then Restart session."
    )

!pip -q install -U pip
# Gemma 3: transformers>=4.50; TRL: SFTConfig; peft: torchao>=0.16 if present.
!pip -q install -U "transformers>=4.50" "trl>=0.14" "torchao>=0.16"
!pip -q install -e ".[gpu]"

# peft>=0.16 raises if stale torchao (e.g. Kaggle 0.10) remains — upgrade then uninstall fallback.
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

INTRO = r'''# ControlSift — Safe free GPU runner (Kaggle / Colab)

**Security**
- Put your Hugging Face token in platform secrets as `HF_TOKEN` only.
- Never paste a token into a cell, chat, or committed file.
- This notebook never prints the token.

**Before you start**
1. Accept the Gemma license on Hugging Face for `google/gemma-3-1b-it`.
2. **Kaggle:** phone-verify → Session options → GPU T4 · Secrets → `HF_TOKEN` ·
   Add data → attach private Dataset built from `controlsift_kaggle_bundle.zip`.
3. **Colab fallback:** Runtime → GPU · Secrets/`getpass` for `HF_TOKEN` ·
   bootstrap downloads the GitHub Release zip automatically.

Keep `SMOKE = True` for the first session.

**After a successful smoke train + torchao fix:** Locate preserves `results/` (adapter survives reclone). Path: **Locate → Install → QLoRA eval → Package** (skip train if adapter still present).
'''


def to_src(text: str) -> list[str]:
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    return lines


def main() -> None:
    nb = json.loads(NB.read_text(encoding="utf-8"))
    nb["cells"][0]["source"] = to_src(INTRO)
    nb["cells"][3]["source"] = to_src(LOCATE)
    nb["cells"][5]["source"] = to_src(INSTALL)
    NB.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    nb2 = json.loads(NB.read_text(encoding="utf-8"))
    s3 = "".join(nb2["cells"][3]["source"])
    s5 = "".join(nb2["cells"][5]["source"])
    assert "stash_workdir_outputs" in s3
    assert "torchao>=0.16" in s5
    assert "Uninstalled torchao" in s5
    print("notebook patched: locate+install+intro")


if __name__ == "__main__":
    main()
