#!/usr/bin/env python3
"""Build report figures from results/ JSON only."""

import json

from controlsift.visualization.charts import build_all_figures


def main() -> None:
    written = build_all_figures()
    print(json.dumps({"ok": True, "figures": written}, indent=2))


if __name__ == "__main__":
    main()
