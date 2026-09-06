#!/usr/bin/env python3
"""Make Locate cell resilient when Config was not run in the kernel."""
from __future__ import annotations

import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "notebooks" / "kaggle_runner.ipynb"
nb = json.loads(p.read_text(encoding="utf-8"))

locate_src = r'''# === Locate or fetch repo (no secrets) ===
# Every run with REPO_URL set: delete WORKDIR, fresh-clone branch tip, print HEAD SHA.
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
        print("Removing existing", dest)
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

if not work.exists():
    raise RuntimeError(f"WORKDIR missing after locate: {work}")

os.chdir(work)
print("WORKDIR =", work.resolve())
assert (work / "data" / "processed" / "train.jsonl").exists(), "missing train.jsonl"
assert (work / "scripts" / "run_gemma_baseline.py").exists(), "missing scripts"
print("Input tree OK")
'''

config_src = r'''# === Config (safe defaults) ===
from pathlib import Path
import os

# Kaggle T4x2: pin one GPU before any torch/CUDA import in later cells.
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")

SMOKE = True          # True = short validation run; False = full test/challenge + train
SMOKE_LIMIT = 16
REPO_URL = "https://github.com/jtflack-grc/controlsift.git"
REPO_BRANCH = "kaggle-bundle"
KAGGLE_DATASET_DIR = "/kaggle/input"

IN_COLAB = Path("/content").exists() and not Path("/kaggle").exists()
WORKDIR = "/content/controlsift" if IN_COLAB else "/kaggle/working/controlsift"

print("SMOKE =", SMOKE)
print("CUDA_VISIBLE_DEVICES =", os.environ.get("CUDA_VISIBLE_DEVICES"))
print("IN_COLAB =", IN_COLAB)
print("REPO_URL =", REPO_URL, "branch", REPO_BRANCH)
print("WORKDIR =", WORKDIR)
'''


def to_lines(s: str) -> list[str]:
    lines = s.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    return lines


updated: list[str] = []
for cell in nb["cells"]:
    if cell.get("cell_type") != "code":
        continue
    src = "".join(cell.get("source", []))
    if src.lstrip().startswith("# === Config (safe defaults) ==="):
        cell["source"] = to_lines(config_src)
        updated.append("Config")
    elif "Locate or fetch repo" in src:
        cell["source"] = to_lines(locate_src)
        updated.append("Locate")

p.write_text(json.dumps(nb, indent=1) + "\n", encoding="utf-8")
print("updated:", updated)

nb2 = json.loads(p.read_text(encoding="utf-8"))
for cell in nb2["cells"]:
    src = "".join(cell.get("source", []))
    if "Locate or fetch repo" in src:
        assert '"WORKDIR" not in globals()' in src
        assert 'setdefault("CUDA_VISIBLE_DEVICES"' in src
        assert "subprocess.run" in src
        assert "check=True" in src
        assert "rev-parse" in src
        assert "WORKDIR missing after locate" in src
        print("Locate OK, chars", len(src))
    if src.lstrip().startswith("# === Config"):
        assert 'setdefault("CUDA_VISIBLE_DEVICES"' in src
        print("Config OK")
