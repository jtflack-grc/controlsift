"""Build MMC show-work notebooks mapped to official DeepMind labs."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

from mmc.labs.paths import ROOT

NOTEBOOKS = ROOT / "mmc" / "notebooks"

SPECS: list[dict] = [
    {
        "file": "week01_ngram.ipynb",
        "title": "Week 1 — N-gram LM + perplexity",
        "gdm": [
            "vendor/ai-foundations/course_1/gdm_lab_1_2_experiment_with_n_gram_models.ipynb",
            "vendor/ai-foundations/course_1/gdm_lab_1_3_compare_n_gram_models_and_transformer_language_models.ipynb",
        ],
        "module": "mmc.labs.week01_ngram",
        "show_keys": ["perplexity", "vocab_size", "sample_generation"],
    },
    {
        "file": "week02_bpe.ipynb",
        "title": "Week 2 — BPE tokenizer + Data Card",
        "gdm": [
            "vendor/ai-foundations/course_2/gdm_lab_2_3_tokenize_texts_into_subword_tokens.ipynb",
            "vendor/ai-foundations/course_2/gdm_lab_2_4_implement_a_bpe_tokenizer.ipynb",
        ],
        "module": "mmc.labs.week02_bpe",
        "show_keys": ["num_merges", "vocab_size", "sample_line_tokens", "data_card"],
    },
    {
        "file": "week04_mlp.ipynb",
        "title": "Week 4 — MLP from scratch",
        "gdm": ["vendor/ai-foundations/course_3/gdm_lab_3_4_design_your_own_mlp.ipynb"],
        "module": "mmc.labs.week04_mlp",
        "show_keys": ["final_loss", "test_accuracy", "weights"],
    },
    {
        "file": "week05_diagnostics.ipynb",
        "title": "Week 5 — Diagnostics (overfit / underfit)",
        "gdm": [
            "vendor/ai-foundations/course_3/gdm_lab_3_5_tune_hyperparameters.ipynb",
            "vendor/ai-foundations/course_3/gdm_lab_3_6_mitigate_overfitting.ipynb",
        ],
        "module": "mmc.labs.week05_diagnostics",
        "show_keys": [
            "underfit_test_acc",
            "overfit_prone_test_acc",
            "healthy_test_acc",
            "dashboard",
        ],
    },
    {
        "file": "week06_transformer.ipynb",
        "title": "Week 6 — Transformer decoder + attention",
        "gdm": [
            "vendor/ai-foundations/course_4/gdm_lab_4_1_attention_visualization.ipynb",
            "vendor/ai-foundations/course_4/gdm_lab_4_2_implement_attention_equation.ipynb",
        ],
        "module": "mmc.labs.week06_transformer",
        "show_keys": ["output_norm", "attention_png", "causal", "heads"],
    },
    {
        "file": "week07_lora.ipynb",
        "title": "Week 7 — LoRA adapter checkpoint",
        "gdm": [
            "vendor/ai-foundations/course_5/gdm_lab_5_5_implement_lora_for_parameter_efficient_fine_tuning.ipynb",
            "vendor/ai-foundations/course_5/gdm_lab_5_6_fine_tune_gemma_with_lora.ipynb",
        ],
        "module": "mmc.labs.week07_lora_scaffold",
        "show_keys": ["status", "rank", "toy_adapter", "production_path"],
    },
    {
        "file": "week09_accelerate.ipynb",
        "title": "Week 9 — Accelerate / GPU memory notes",
        "gdm": [
            "vendor/ai-foundations/course_7/gdm_lab_7_4_estimate_gpu_memory.ipynb",
            "vendor/ai-foundations/course_7/gdm_lab_7_5_fine_tune_a_model_with_bfloat16.ipynb",
            "vendor/ai-foundations/course_7/gdm_lab_7_6_apply_gradient_accumulation.ipynb",
        ],
        "module": None,
        "markdown_extra": (
            "Course 7 labs are the official accelerate checkbox. "
            "ControlSift packaging: `notebooks/KAGGLE_SAFE_RUN.md` + `notebooks/kaggle_runner.ipynb`. "
            "Open the GDM notebooks under `vendor/ai-foundations/course_7/` in Jupyter/Colab, "
            "then fill memory numbers into `mmc/deliverables/week09_accelerate.md` after a real GPU run."
        ),
    },
    {
        "file": "week11_comparative.ipynb",
        "title": "Week 11 — Training & comparative analysis",
        "gdm": [
            "vendor/ai-foundations/course_8/gdm_lab_8_1_classification_worked_example.ipynb",
            "vendor/ai-foundations/course_8/gdm_lab_8_3_classification_stage_3_train_and_evaluate_your_model.ipynb",
        ],
        "module": "mmc.labs.week11_comparative",
        "show_keys": ["rows", "weights", "notes"],
    },
]


def _md(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": uuid.uuid4().hex[:8],
        "metadata": {},
        "source": [line + "\n" for line in source.strip("\n").split("\n")],
    }


def _code(source: str) -> dict:
    return {
        "cell_type": "code",
        "id": uuid.uuid4().hex[:8],
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.strip("\n").split("\n")],
    }


def build_one(spec: dict) -> dict:
    gdm_lines = "\n".join(f"- `{p}`" for p in spec["gdm"])
    cells = [
        _md(
            f"""# {spec["title"]}

**MMC / DeepMind track** — show-work notebook.

### How to run

- **Local (Anaconda):** from repo root  
  `conda activate controlsift-mmc` then `powershell -File scripts/start_mmc_jupyter.ps1`  
  or open this file in JupyterLab and use kernel **Python (controlsift-mmc)**.
- **GitHub Pages cannot execute notebooks** (static hosting only). After the repo is on GitHub, use **Open in Colab** / Binder links on the deliverables hub, or clone and run locally.

## Official DeepMind labs (checkbox)

{gdm_lines}

Full map: `mmc/GDM_LAB_MAP.md`. Upstream clone: `vendor/ai-foundations/`.

## ControlSift exceed path

Run the cells below to regenerate **this repo's** graded artifacts under `mmc/deliverables/outputs/`.
Do not invent Gemma metrics; leave GPU rows null until a real HF/Kaggle run."""
        ),
        _code(
            """from pathlib import Path
import os
import sys

# Resolve repo root whether Jupyter cwd is repo root or mmc/notebooks/
here = Path.cwd().resolve()
root = None
for candidate in [here, *here.parents]:
    if (candidate / "mmc" / "labs").is_dir() and (candidate / "mmc" / "notebooks").is_dir():
        root = candidate
        break
if root is None:
    raise RuntimeError("Could not find ControlSift repo root (expected mmc/labs/). Open Jupyter from the repo.")
os.chdir(root)
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
print("cwd:", Path.cwd())
print("python:", sys.executable)"""
        ),
    ]
    if spec.get("markdown_extra"):
        cells.append(_md(spec["markdown_extra"]))
    if spec.get("module"):
        keys = spec.get("show_keys") or []
        keys_repr = ", ".join(repr(k) for k in keys)
        cells.append(
            _code(
                f"""from {spec["module"]} import run
import json

result = run()
show = {{k: result.get(k) for k in [{keys_repr}]}} if [{keys_repr}] else result
print(json.dumps(show, indent=2, default=str))
result"""
            )
        )
        cells.append(
            _md(
                """### Next

1. Open the matching official GDM notebook under `vendor/ai-foundations/` and complete it on Skills/Colab if your cohort requires the upstream lab.
2. Confirm artifacts landed in `mmc/deliverables/outputs/`.
3. Sync the public hub: `python -m mmc.labs.sync_artifacts`."""
            )
        )
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python (controlsift-mmc)",
                "language": "python",
                "name": "controlsift-mmc",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
            "controlsift": {
                "gdm_labs": spec["gdm"],
                "mmc_module": spec.get("module"),
            },
        },
        "cells": cells,
    }


def main() -> None:
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    index_rows = []
    for spec in SPECS:
        path = NOTEBOOKS / spec["file"]
        path.write_text(json.dumps(build_one(spec), indent=1) + "\n", encoding="utf-8")
        print("wrote", path)
        index_rows.append(f"| {spec['file']} | {spec['title']} |")
    # Keep the hand-written runbook if present; only seed a stub when missing.
    readme = NOTEBOOKS / "README.md"
    if not readme.is_file():
        readme.write_text(
            f"""# MMC show-work notebooks

See `environment-mmc.yml` and `scripts/start_mmc_jupyter.ps1` for local Anaconda runs.

| Notebook | Title |
|----------|-------|
{chr(10).join(index_rows)}
""",
            encoding="utf-8",
        )
        print("wrote", readme)


if __name__ == "__main__":
    main()
