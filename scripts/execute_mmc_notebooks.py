"""Execute MMC show-work notebooks headlessly (smoke test)."""

from __future__ import annotations

import sys
from pathlib import Path

from nbclient import NotebookClient
from nbformat import read, write

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "mmc" / "notebooks"


def execute_one(path: Path) -> None:
    nb = read(path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=120,
        kernel_name="python3",
        resources={"metadata": {"path": str(ROOT)}},
    )
    # Ensure repo root imports (mmc.*)
    client.execute(cwd=str(ROOT))
    out = path.with_name(path.stem + ".executed.ipynb")
    write(nb, out)
    print("ok", path.name, "→", out.name)


def main() -> int:
    sys.path.insert(0, str(ROOT))
    targets = sorted(NB_DIR.glob("week*.ipynb"))
    if not targets:
        print("no notebooks in", NB_DIR, file=sys.stderr)
        return 1
    # Skip week09 (no runnable module) for smoke by default unless --all
    all_flag = "--all" in sys.argv
    for path in targets:
        if path.name.startswith("week09") and not all_flag:
            print("skip", path.name, "(notes-only; pass --all to run)")
            continue
        print("executing", path.name, "...")
        execute_one(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
