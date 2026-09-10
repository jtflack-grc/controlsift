# Week 10 deliverable — Capstone Research Proposal & baseline pipeline

**Handbook:** Course 08 · Capstone – Setup & Formulation  
**Key deliverable:** Peer-reviewed Capstone Research Proposal & baseline pipeline

## 1. Research problem

**Title:** ControlSift — Can a small language model help under-resourced teams tell proof from paperwork?

**MMC rubric option:** Goal 4 — Reduced Inequalities  
**Official UN designation:** SDG 10 — Reduced Inequalities

**Question:** Can small-model approaches classify cybersecurity evidence quality across five classes, and does QLoRA improve on prompted Gemma baselines under a controlled experiment?

## 2. Objectives (measurable)

1. Ship a leakage-controlled synthetic benchmark with family-isolated splits and deterministic generation.
2. Establish classical floors (majority, TF-IDF) before interpreting language-model results.
3. Freeze evaluation protocol before final model claims.
4. Compare Gemma zero-shot, few-shot, and QLoRA using macro F1 and output reliability.
5. Publish Failure Lab + assurance artifacts; preserve negative results and claim boundaries.

## 3. Dataset & Data Card

The hardened classical benchmark is dataset **v1.1.0**, approximately 1,500 cases across five balanced classes. Labels are rule-derived with structural/scripted audit support; the corpus is synthetic only. Data Card: `governance/DATA_CARD.md` and `docs/assurance/data-card.html`.

Pipeline: `src/controlsift/data/generate.py` → `data/processed/` → validators → protocol seal.

## 4. Baseline and final experiment record

```bash
pip install -e ".[dev]"
python scripts/validate_dataset.py
python scripts/run_tfidf_baseline.py
python scripts/run_evaluation.py
pytest
```

| Experiment | Dataset | Test macro F1 | Challenge macro F1 | Status |
|------------|---------|---------------|--------------------|--------|
| Majority | v1.1.0 | 0.067 | 0.067 | complete |
| TF-IDF + LR | v1.1.0 | ~0.533 | ~0.524 | complete |
| Gemma zero-shot | v1.0.0 | ~0.080 | ~0.105 | complete |
| Gemma few-shot | v1.0.0 | ~0.137 | ~0.174 | complete |
| Gemma QLoRA | v1.0.0 | ~0.083 | ~0.131 | complete |

**Final execution boundary:** the classical experiments use v1.1.0 while the Gemma experiments use v1.0.0. Within-version comparisons are controlled; cross-version values are descriptive only and are not presented as a same-benchmark classical-vs-Gemma ranking.

Within the controlled Gemma v1.0 experiments, few-shot prompting is strongest. QLoRA does not beat few-shot and test parse success is about 0.435.

## 5. Compute and execution path

- Gemma family: Gemma 3 1B
- Parameter-efficient adaptation: QLoRA configuration in `configs/gemma3_1b_qlora.yaml`
- Free-tier execution support: Kaggle/Hugging Face tooling under `notebooks/` and `scripts/`
- Secrets: `HF_TOKEN` stored through platform secret handling, not committed to the repository
- Result receipts: `results/gemma_zero_shot/`, `results/gemma_few_shot/`, and `results/gemma_qlora/`

## 6. Proposal outcome

The proposed research pipeline was completed. The final artifact preserves two important findings that were not assumed in advance: benchmark hardening materially reduced the original TF-IDF shortcut, and QLoRA did not automatically improve Gemma performance. Final review also surfaced the dataset-version boundary, which is disclosed throughout the capstone rather than hidden behind a cleaner but unsupported leaderboard.

## 7. Links

- Methods: `docs/capstone/methods-evidence.html`
- Full narrative: `docs/capstone/paper.html`
- Protocol: `governance/PROTOCOL.md`
- Results: `docs/results.html`
