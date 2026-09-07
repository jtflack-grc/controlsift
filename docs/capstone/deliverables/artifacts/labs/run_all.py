"""Run MMC weekly lab deliverables 1–2, 4–7 and regenerate dashboards."""

from __future__ import annotations

import json

from mmc.labs import (
    build_notebooks,
    build_week_pages,
    sync_artifacts,
    week01_ngram,
    week02_bpe,
    week04_mlp,
    week05_diagnostics,
    week06_transformer,
    week07_lora_scaffold,
    week11_comparative,
)


def main() -> None:
    build_notebooks.main()
    results = {
        "week01": week01_ngram.run(),
        "week02": week02_bpe.run(),
        "week04": week04_mlp.run(),
        "week05": week05_diagnostics.run(),
        "week06": week06_transformer.run(),
        "week07": week07_lora_scaffold.run(),
        "week11": week11_comparative.run(),
    }
    sync_artifacts.run()
    build_week_pages.main()
    print(json.dumps({k: {"ok": True, **{kk: vv for kk, vv in v.items() if kk != "sample_generation"}} for k, v in results.items()}, indent=2))


if __name__ == "__main__":
    main()
