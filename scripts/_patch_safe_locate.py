#!/usr/bin/env python3
"""Patch kaggle_runner.ipynb Locate cell for safe temp-fetch + zip fallback."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB_PATH = ROOT / "notebooks" / "kaggle_runner.ipynb"

INTRO = '''# ControlSift — Safe free GPU runner (Kaggle / Colab)

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

**If adapter already exists and you only need the torchao fix — skip Locate:**
```
!pip -q install -U "torchao>=0.16"
```
then run **Install (if needed) → QLoRA eval → Package**. Do not re-run Locate.

**After a successful smoke train + code refresh:** Locate fetches into a temp dir first
(never deletes live WORKDIR until success), preserves `results/`, and falls back to the
Release zip if git fails. Path: **Locate → Install → QLoRA eval → Package**
(skip train if adapter still present).
'''

LOCATE = r'''# === Locate or fetch repo (no secrets) ===
# Safe refresh: never rmtree live WORKDIR until a new tree is ready.
# Fetch order: git --branch → git default+checkout → Release zip.
# Preserves WORKDIR/results (adapter) across refresh. NameError-proof defaults.
import hashlib
import os
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")

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

BUNDLE_URL = (
    "https://github.com/jtflack-grc/controlsift/releases/download/"
    "kaggle-bundle/controlsift_kaggle_bundle.zip"
)

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
fetch_root = work.parent / "_controlsift_fetch"
PRESERVE_RELPATHS = ("results",)


def _stash_dir() -> Path:
    return work.parent / "_controlsift_preserve"


def stash_workdir_outputs(dest: Path):
    """Copy results/ aside before replacing WORKDIR."""
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


def restore_workdir_outputs(dest: Path, stash) -> None:
    """Merge stashed results/ back after successful replace (stashed wins)."""
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


def adapter_present(dest: Path) -> bool:
    return (dest / "results" / "gemma_qlora" / "adapter").exists()


def find_bundled_repo(root: Path):
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


def _run_git(cmd, cwd=None):
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    print(">>", " ".join(cmd))
    try:
        proc = subprocess.run(
            cmd,
            check=True,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "git not found on PATH. On Kaggle, Internet must be ON and git available."
        ) from exc
    except subprocess.CalledProcessError as exc:
        print("STDOUT:", (exc.stdout or "")[-2000:])
        print("STDERR:", (exc.stderr or "")[-2000:])
        raise
    if proc.stdout:
        print(proc.stdout[-2000:])
    if proc.stderr:
        print(proc.stderr[-2000:])
    return proc


def _git_head(dest: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(dest), "rev-parse", "HEAD"], text=True
    ).strip()


def fetch_via_git_branch(url: str, branch: str, dest: Path) -> str:
    _run_git(["git", "clone", "--depth", "1", "--branch", branch, url, str(dest)])
    sha = _git_head(dest)
    print(f"Git branch clone OK HEAD={sha}")
    return sha


def fetch_via_git_checkout(url: str, branch: str, dest: Path) -> str:
    _run_git(["git", "clone", "--depth", "1", url, str(dest)])
    try:
        _run_git(["git", "fetch", "--depth", "1", "origin", branch], cwd=str(dest))
        _run_git(["git", "checkout", branch], cwd=str(dest))
    except subprocess.CalledProcessError:
        _run_git(["git", "checkout", "-B", branch, f"origin/{branch}"], cwd=str(dest))
    sha = _git_head(dest)
    print(f"Git default+checkout OK HEAD={sha}")
    return sha


def fetch_via_release_zip(dest: Path) -> str:
    zip_path = dest.parent / "_controlsift_bundle.zip"
    extract_to = dest.parent / "_controlsift_zip_extract"
    if zip_path.exists():
        zip_path.unlink()
    if extract_to.exists():
        shutil.rmtree(extract_to)
    extract_to.mkdir(parents=True)
    print("Downloading Release zip:", BUNDLE_URL)
    try:
        urllib.request.urlretrieve(BUNDLE_URL, zip_path)
    except Exception as exc:
        raise RuntimeError(
            f"Release zip download failed ({type(exc).__name__}: {exc}). "
            "Confirm Internet ON, or attach Dataset / upload zip."
        ) from exc
    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()[:16]
    print(f"Zip bytes={zip_path.stat().st_size} sha256_16={digest}")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_to)
    src = find_bundled_repo(extract_to)
    if src is None:
        raise RuntimeError("Release zip missing controlsift pyproject.toml")
    shutil.copytree(src, dest)
    print(f"Release zip extract OK digest={digest}")
    return f"zip:{digest}"


def fetch_repo_tree(url: str, branch: str, dest: Path) -> str:
    """Populate dest with a fresh tree. Never touches live WORKDIR."""
    if dest.exists():
        shutil.rmtree(dest)
    errors = []
    for name, fn in (
        ("git clone --branch", lambda: fetch_via_git_branch(url, branch, dest)),
        ("git clone + checkout", lambda: fetch_via_git_checkout(url, branch, dest)),
        ("release zip", lambda: fetch_via_release_zip(dest)),
    ):
        if dest.exists():
            shutil.rmtree(dest)
        try:
            print(f"--- try: {name} ---")
            return fn()
        except Exception as exc:
            msg = f"{name} failed: {type(exc).__name__}: {exc}"
            print(msg)
            errors.append(msg)
            if dest.exists():
                shutil.rmtree(dest, ignore_errors=True)
    raise RuntimeError("All fetch strategies failed.\n" + "\n".join(errors))


def replace_workdir(live: Path, fetched: Path) -> None:
    """Swap live WORKDIR only after fetched tree is ready."""
    backup = live.parent / "_controlsift_old"
    if backup.exists():
        shutil.rmtree(backup)
    if live.exists():
        live.rename(backup)
    try:
        fetched.rename(live)
    except Exception:
        if backup.exists() and not live.exists():
            backup.rename(live)
            print("keeping existing tree (rename failed; restored backup)")
        raise
    if backup.exists():
        shutil.rmtree(backup, ignore_errors=True)


# --- main locate flow ---
ref_id = None
preserved = None
had_existing = work.exists()

try:
    if REPO_URL:
        preserved = stash_workdir_outputs(work)
        ref_id = fetch_repo_tree(REPO_URL, REPO_BRANCH, fetch_root)
        replace_workdir(work, fetch_root)
        restore_workdir_outputs(work, preserved)
        preserved = None
    else:
        extract_input_zips(Path(KAGGLE_DATASET_DIR))
        src = find_bundled_repo(Path(KAGGLE_DATASET_DIR))
        if src is None:
            src = find_bundled_repo(Path("/kaggle/working/_extracted_dataset"))
        if src is not None:
            preserved = stash_workdir_outputs(work)
            if fetch_root.exists():
                shutil.rmtree(fetch_root)
            shutil.copytree(src, fetch_root)
            replace_workdir(work, fetch_root)
            restore_workdir_outputs(work, preserved)
            preserved = None
            ref_id = f"dataset:{src}"
            print("Copied dataset bundle from", src)
        elif Path("/content/controlsift").exists():
            work = Path("/content/controlsift")
            ref_id = "existing:/content/controlsift"
            print("Using existing /content/controlsift")
        else:
            raise RuntimeError(
                "Could not find ControlSift. Set REPO_URL or attach the Dataset zip."
            )
except Exception as exc:
    # Critical: leave existing WORKDIR intact on failure.
    if fetch_root.exists():
        shutil.rmtree(fetch_root, ignore_errors=True)
    if had_existing and work.exists():
        print(
            f"Locate failed ({type(exc).__name__}: {exc}). "
            f"keeping existing tree at {work}"
        )
        print(
            "Adapter present:",
            adapter_present(work),
            work / "results" / "gemma_qlora" / "adapter",
        )
        print(
            "Workaround if you only need torchao: "
            '!pip -q install -U "torchao>=0.16" then run Eval (skip Locate).'
        )
        if (work / "pyproject.toml").exists():
            ref_id = "kept-existing"
        else:
            raise
    else:
        raise

if not work.exists():
    raise RuntimeError(f"WORKDIR missing after locate: {work}")

os.chdir(work)
print("WORKDIR =", work.resolve())
print("REF =", ref_id)
print("Adapter present:", adapter_present(work), work / "results" / "gemma_qlora" / "adapter")
assert (work / "data" / "processed" / "train.jsonl").exists(), "missing train.jsonl"
assert (work / "scripts" / "run_gemma_baseline.py").exists(), "missing scripts"
print("Input tree OK")
'''


def to_source_lines(text: str) -> list[str]:
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    return lines


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding="utf-8"))
    nb["cells"][0]["source"] = to_source_lines(INTRO)
    nb["cells"][3]["source"] = to_source_lines(LOCATE)
    nb["cells"][3]["outputs"] = []
    nb["cells"][3]["execution_count"] = None
    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    src = "".join(nb["cells"][3]["source"])
    assert "_controlsift_fetch" in src
    assert "keeping existing tree" in src
    assert "release zip" in src
    assert "torchao>=0.16" in "".join(nb["cells"][0]["source"])
    # Must not delete live work before fetch succeeds
    assert "Removing existing" not in src
    print(f"Patched {NB_PATH}")
    print(f"Locate cell chars: {len(src)}")


if __name__ == "__main__":
    main()
