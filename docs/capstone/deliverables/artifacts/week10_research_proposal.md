# Week 10 deliverable — Capstone Research Proposal & baseline pipeline

**Handbook:** Course 08 · Capstone – Setup & Formulation  
**Key deliverable:** Peer-reviewed Capstone Research Proposal & baseline pipeline

## 1. Research problem

**Title:** ControlSift — Can a small language model help under-resourced teams tell proof from paperwork?

**Official SDG:** Goal 10 (Reduced Inequalities) — unequal access to high-quality GRC evidence review.

**Question:** Does QLoRA domain adaptation of Gemma 3 1B Instruct improve five-class cybersecurity evidence-quality classification on a sealed synthetic benchmark, relative to classical and prompted baselines?

## 2. Objectives (measurable)

1. Ship a leakage-controlled synthetic benchmark (family-isolated splits, seed 42).
2. Establish classical floors (majority, TF-IDF) before LLM claims.
3. Freeze evaluation protocol (`protocol-v1-locked`) before Gemma runs.
4. Compare zero-shot, few-shot, and QLoRA on macro F1 (test + challenge).
5. Publish Failure Lab + Assurance artifacts; no fabricated metrics.

## 3. Dataset & Data Card

| Item | Value |
|------|-------|
| Version | 1.1.0 |
| Size | 1,500 cases · 5 balanced classes |
| Splits | 1000 / 200 / 200 / 100 |
| Labels | Rule-derived + structural/scripted audit |
| Privacy | Synthetic only |
| Data Card | `governance/DATA_CARD.md` · `docs/assurance/data-card.html` |

Pipeline: `src/controlsift/data/generate.py` → `data/processed/` → validators → protocol seal.

## 4. Baseline pipeline (reproducible)

```bash
pip install -e ".[dev]"
python scripts/validate_dataset.py
python scripts/run_tfidf_baseline.py
python scripts/run_evaluation.py
pytest
```

| Baseline | Test macro F1 | Challenge macro F1 | Status |
|----------|---------------|--------------------|--------|
| Majority | 0.067 | 0.067 | complete |
| TF-IDF + LR | ~0.53 | ~0.52 | complete |
| Gemma zero-shot | null | null | pending GPU |
| Gemma few-shot | null | null | pending GPU |
| Gemma QLoRA | null | null | pending GPU |

## 5. GPU environment plan

- Primary: Kaggle free GPU via `notebooks/kaggle_runner.ipynb`
- Packaging: `scripts/package_for_kaggle.py`
- Secrets: `HF_TOKEN` in platform Secrets only
- Guide: `notebooks/KAGGLE_SAFE_RUN.md`

## 6. Proposal status

`complete` for formulation + classical baselines. Peer review = MMC mentor / cohort feedback on this document + public site.

## 7. Links

- Methods: `docs/capstone/methods-evidence.html`
- Full narrative: `docs/capstone/paper.html`
- Protocol: `governance/PROTOCOL.md`
