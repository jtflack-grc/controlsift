# ControlSift

**Can a small AI model tell proof from paperwork?**

Domain adaptation of Gemma 3 for cybersecurity control-evidence assessment — with research integrity, failure analysis, and reproducible receipts.

> Status: **framework complete; modeling pending gated GPU access**. Classical baselines and public research site are live. Staying on the original Gemma 3 + QLoRA path — see [`reports/TWELVE_WEEK_RUNWAY.md`](reports/TWELVE_WEEK_RUNWAY.md). Charter: [`ControlSift.md`](ControlSift.md).

## Why this matters

Cybersecurity and GRC teams routinely confuse *artifacts* with *proof*. A policy requiring MFA is not proof MFA is enabled. An IAM export showing a privileged user without MFA can *contradict* the control.

ControlSift asks whether parameter-efficient fine-tuning (QLoRA) can improve a small language model's ability to make these distinctions on a controlled synthetic benchmark.

## Evidence example

**Control:** Privileged accounts must use multi-factor authentication.

| Evidence | Expected |
|----------|----------|
| Audit-period export of all privileged accounts showing MFA enrollment for each | **SUFFICIENT** |
| Policy stating MFA is required for privileged accounts | **INSUFFICIENT** |

## Research question

Can parameter-efficient fine-tuning materially improve a small general-purpose language model's ability to evaluate the sufficiency and relevance of cybersecurity control evidence?

## Benchmark

- ~1,500 synthetic cases across five classes: SUFFICIENT, PARTIAL, INSUFFICIENT, IRRELEVANT, CONTRADICTORY
- Splits: train 1000 / validation 200 / test 200 / challenge 100
- Scenario-family isolation (no family leakage across splits)
- Canonical seed: `42`

## Model ladder

```text
Majority → TF-IDF+LR → Gemma zero-shot → Gemma few-shot → Gemma QLoRA
```

Primary metric: **macro F1**.

## Key results

| Experiment | Test macro F1 | Challenge macro F1 |
|------------|---------------|--------------------|
| Majority | ~0.20 | ~0.20 |
| TF-IDF + LR | ~0.86 | ~0.78 |
| Gemma zero-shot | pending | pending |
| Gemma few-shot | pending | pending |
| Gemma QLoRA | pending | pending |

Machine-readable sources: `results/*/metrics_*.json` → `docs/data/results.json`. Never invent numbers.

Gate 1: an earlier generator revision let TF-IDF saturate at 1.0; mutations were hardened (minimal edits + surface noise) before protocol seal.

## What still fails

TF-IDF residual errors concentrate on **PARTIAL ↔ SUFFICIENT** coverage boundaries. Failure Lab: [`docs/failure-lab.html`](docs/failure-lab.html). LLM failure modes pending GPU runs.

## Explore

- [Public research site](docs/index.html) (GitHub Pages)
- [Failure Lab](docs/failure-lab.html)
- [Reproduce](docs/reproduce.html)
- [Responsible AI](docs/responsible-ai.html)
- Master charter: [`ControlSift.md`](ControlSift.md)

## Methodology (short)

1. Deterministic synthetic evidence generation with rule-derived labels
2. Family-level split isolation and integrity tests
3. Classical and prompting baselines
4. Gemma 3 1B IT + QLoRA on free GPU (Kaggle / Colab)
5. Held-out + challenge evaluation, slices, statistics, error analysis
6. Data Card, Model Card, AI risk register

## Reproduction

```bash
python -m venv .venv
pip install -e ".[dev]"
python scripts/generate_dataset.py
python scripts/validate_dataset.py
python scripts/run_tfidf_baseline.py
pytest
```

Gemma training and inference use free Kaggle/Colab GPUs. **Safe path:** [`notebooks/KAGGLE_SAFE_RUN.md`](notebooks/KAGGLE_SAFE_RUN.md) + [`notebooks/kaggle_runner.ipynb`](notebooks/kaggle_runner.ipynb). Token stays in platform Secrets as `HF_TOKEN` — never in git.

## Responsible use

ControlSift is **not** an automated auditor, compliance engine, or replacement for human judgment. Labels are rule-derived on synthetic data. See `governance/`.

## Repository structure

See Section 46 of `ControlSift.md`. Package code lives under `src/controlsift/`.

## Acknowledgements

Independent research project. Mentor Me Collective / DeepMind curriculum context (if any) does not define the public identity of ControlSift.
