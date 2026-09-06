# ControlSift

**Can a small AI model tell proof from paperwork?**

Domain adaptation of Gemma 3 for cybersecurity control-evidence assessment — with research integrity, failure analysis, and reproducible receipts.

> Status: **classical stage locked (dataset v1.1.0; tag `protocol-v1-locked` seals data/prompt — see [`governance/TAGS.md`](governance/TAGS.md)); Gemma modeling pending gated HF/Kaggle access**. Runway: [`reports/TWELVE_WEEK_RUNWAY.md`](reports/TWELVE_WEEK_RUNWAY.md). Charter: [`ControlSift.md`](ControlSift.md).

## Why this matters

Cybersecurity and GRC teams routinely confuse *artifacts* with *proof*. A policy requiring MFA is not proof MFA is enabled. An IAM export showing a privileged user without MFA can *contradict* the control.

ControlSift asks whether parameter-efficient fine-tuning (QLoRA) can improve a small language model's ability to make these distinctions on a **controlled synthetic benchmark**.

## Research surface (read this)

Dataset **v1.1** is a **compositional evidence-packet** benchmark: dual sections, shared decoys, `SCOPE` coverage integers, substance pointers, and `ROW_DETAIL` conflicts — hardened so bag-of-words no longer saturates. It measures whether models can read those compositional cues, **not** scoring of raw customer binders. Decision record: [`governance/RESEARCH_SURFACE.md`](governance/RESEARCH_SURFACE.md).

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
- Dataset version: **1.1.0**

## Model ladder

```text
Majority → TF-IDF+LR → Gemma zero-shot → Gemma few-shot → Gemma QLoRA
```

Primary metric: **macro F1**.

## Key results

| Experiment | Test macro F1 | Challenge macro F1 |
|------------|---------------|--------------------|
| Majority | **0.067** | 0.067 |
| TF-IDF + LR | **~0.53** | **~0.52** |
| Gemma zero-shot | `null` | `null` |
| Gemma few-shot | `null` | `null` |
| Gemma QLoRA | `null` | `null` |

Machine-readable sources: `results/*/metrics_*.json` → `docs/data/results.json`. Never invent numbers.

**Note:** Majority **accuracy** on a balanced 5-way task is 0.20; **macro F1** is ~0.067. Do not conflate them.

Gate 1: early generator drafts let TF-IDF saturate at 1.0; v1.1 compositional packing + surface harden brought test macro F1 to ~0.53 before protocol seal.

## Label audit (not “fully human-labeled”)

- **100% challenge** + stratified sample: structural integrity audit (`structural_auditor_v1`)
- **20 challenge cases** (4/label): **scripted** spot-check notes (`spotcheck_v1`) — see [`reports/SPOTCHECK_20.md`](reports/SPOTCHECK_20.md)
- Primary labels remain **rule-derived**

## What still fails (classical)

TF-IDF is weakest on **SUFFICIENT / IRRELEVANT / PARTIAL** compositional cues; **CONTRADICTORY** remains easier (~0.93 F1). Failure Lab: [`docs/failure-lab.html`](docs/failure-lab.html). LLM failure modes pending GPU runs.

## Explore

- [Public research site](docs/index.html) (GitHub Pages)
- [Failure Lab](docs/failure-lab.html)
- [Reproduce](docs/reproduce.html)
- [Assurance](docs/assurance.html)
- Master charter: [`ControlSift.md`](ControlSift.md)

## Methodology (short)

1. Deterministic synthetic evidence generation with rule-derived labels
2. Family-level split isolation and integrity tests
3. Classical baselines + lexical ceiling test
4. Gemma 3 1B IT + QLoRA on free GPU (Kaggle / Colab)
5. Held-out + challenge evaluation, slices, statistics, error analysis
6. Data Card, Model Card, AI risk register

## CRISP-DM mapping (GCLP GitHub structure)

| CRISP-DM step | ControlSift |
|---------------|-------------|
| Business understanding | SDG 10 problem: unequal access to honest evidence review (`docs/capstone/`) |
| Data understanding | `notebooks/01_dataset_exploration.ipynb`, Data Card, `data/raw/` note |
| Data preparation | Generator → `data/processed/`; validators; protocol seal |
| Modeling | `notebooks/02_traditional_baseline.ipynb` … `04_gemma_qlora_training.ipynb` |
| Evaluation | `notebooks/05_final_evaluation.ipynb`, `06_error_analysis.ipynb`, Results / Failure Lab |
| Deployment | Out of scope for v1 (research artifact + public site only) |

Reflection: [`reflection/project_reflection.md`](reflection/project_reflection.md).

## Reproduction

```bash
python -m venv .venv
pip install -e ".[dev]"
python scripts/validate_dataset.py
python scripts/run_tfidf_baseline.py
pytest
```

Gemma training and inference use free Kaggle/Colab GPUs. **Safe path:** [`notebooks/KAGGLE_SAFE_RUN.md`](notebooks/KAGGLE_SAFE_RUN.md) + [`notebooks/kaggle_runner.ipynb`](notebooks/kaggle_runner.ipynb). Token stays in platform Secrets as `HF_TOKEN` — never in git.

Package without secrets:

```bash
python scripts/package_for_kaggle.py
```

## Responsible use

ControlSift is **not** an automated auditor, compliance engine, or replacement for human judgment. Labels are rule-derived on synthetic data. See `governance/`.

## Repository structure

Aligned with GCLP Capstone GitHub guidance plus research layout:

```text
README.md · requirements.txt
data/raw/ · data/processed/ · data/scenarios/
notebooks/01_…–06_… · notebooks/kaggle_runner.ipynb
reports/figures/ · reflection/project_reflection.md
src/controlsift/ · scripts/ · governance/ · docs/ · docs/capstone/
```

See also Section 46 of `ControlSift.md`.

## Acknowledgements

Independent applied research project developed in the Mentor Me Collective / DeepMind AI Research Foundations context. Official GCLP capstone SDG selection: **Goal 10**.
