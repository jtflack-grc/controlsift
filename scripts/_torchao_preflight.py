"""Shared torchao/peft compatibility helper for Gemma GPU scripts.

peft>=0.16 raises ImportError if torchao is installed but <0.16.
Upgrade first; uninstall as fallback so PeftModel.from_pretrained can load.
Never prints secrets.
"""

from __future__ import annotations

import importlib.metadata as md
import subprocess
import sys


def _parse_ver(ver: str) -> tuple[int, int, int]:
    parts: list[int] = []
    for chunk in ver.split("."):
        digits = ""
        for ch in chunk:
            if ch.isdigit():
                digits += ch
            else:
                break
        if not digits:
            break
        parts.append(int(digits))
        if len(parts) == 3:
            break
    while len(parts) < 3:
        parts.append(0)
    return parts[0], parts[1], parts[2]


def ensure_torchao_compatible() -> None:
    """Make torchao safe for peft, or remove it if upgrade fails."""
    try:
        ver = md.version("torchao")
    except md.PackageNotFoundError:
        print("torchao: not installed (ok for peft)")
        return

    if _parse_ver(ver) >= (0, 16, 0):
        print(f"torchao: {ver} (ok)")
        return

    print(f"torchao: {ver} incompatible with peft (need >=0.16); upgrading…")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-U", "torchao>=0.16"],
        check=False,
    )
    try:
        ver2 = md.version("torchao")
    except md.PackageNotFoundError:
        ver2 = None
    if ver2 and _parse_ver(ver2) >= (0, 16, 0):
        print(f"torchao: upgraded to {ver2}")
        return

    print("torchao: upgrade failed; uninstalling so peft can load")
    subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "-y", "torchao"],
        check=False,
    )
