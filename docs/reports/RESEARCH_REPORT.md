# ControlSift Research Report

**Working question:** Can a small AI model tell proof from paperwork?  
**Technical title:** Domain Adaptation of Gemma 3 for Cybersecurity Control-Evidence Assessment  
**Dataset:** v1.1.0 (compositional packet packing + AFLite-style surface harden)  
**Protocol tag:** `protocol-v1-locked`

## Abstract

ControlSift asks whether QLoRA adaptation of Gemma 3 1B IT improves five-class judgment of cybersecurity evidence quality (SUFFICIENT / PARTIAL / INSUFFICIENT / IRRELEVANT / CONTRADICTORY). Before any GPU run, the project treats data integrity as the first result: a deterministic synthetic benchmark with family-isolated splits, classical baselines, human-review audit of the challenge set, and a public site that refuses fabricated LLM metrics. Dataset v1.1 was hardened until TF-IDF+LR falls to an uncomfortable ~0.53 test macro F1 (challenge ~0.52), so lexical shortcuts no longer saturate the task.

## 1. Introduction

Security assurance still depends on humans distinguishing operational proof from binder filler. Small instruction-tuned models are attractive for assisted review, but only if gains over classical text baselines are real. ControlSift freezes a protocol, seals evaluation splits, and climbs a method ladder: majority → TF-IDF → Gemma zero-shot → few-shot → QLoRA.

## 2. Benchmark

| Item | Value |
|------|-------|
| Cases | 1,500 (balanced, 300/label) |
| Splits | train 1000 / validation 200 / test 200 / challenge 100 |
| Domains | 13 |
| Seed | 42 |
| Split rule | scenario-family isolation |
| Labels | rule-derived mutations over shared sufficient scaffolds |

v1.1 representation packs each case as dual sections (Mercury/Neon) holding both a claim-like text and a near-domain distractor, plus identical `SCOPE` scaffolding and shared decoy lexicons. Class signal is compositional (substance pointer, inventory vs `file_rows`, epistemic hedges, `ROW_DETAIL` conflicts), not a unique cue phrase per label.

Human review: structural audit of **100% challenge** + stratified development sample (`data/review_log.csv`, `reports/HUMAN_REVIEW_AUDIT.md`).

## 3. Methods

**Ladder.** Majority class; TF-IDF (1–2 grams) + balanced logistic regression; Gemma 3 1B IT zero/few-shot; QLoRA (4-bit NF4, r=16, α=16).

**Prompt / parse.** Canonical template in `src/controlsift/prompting/templates.py`; robust JSON/label parse with `UNPARSEABLE` fallback.

**Primary metric.** Macro F1; bootstrap CIs on test; challenge reported separately.

**Integrity checks.** Schema/balance/leakage tests; TF-IDF ceiling test (`tests/test_lexical_ceiling.py`); protocol seal hashes in `governance/PROTOCOL_SEAL.json`.

## 4. Results (classical stage)

| Experiment | Test macro F1 | Challenge macro F1 | Notes |
|------------|---------------|--------------------|-------|
| Majority | **0.067** | 0.067 | Accuracy 0.20 on balanced 5-way; macro F1 ≠ accuracy |
| TF-IDF + LR | **~0.53** | **~0.52** | After v1.1 harden (was ~0.86 / saturated 1.0 earlier) |
| Gemma zero-shot | `null` | `null` | Pending HF/Kaggle |
| Gemma few-shot | `null` | `null` | Pending |
| Gemma QLoRA | `null` | `null` | Pending |

Learning curve (TF-IDF on test): macro F1 rises from ~0.21 @100 train rows to ~0.53 @1000 — data helps, but the task stays non-trivial.

### Confusion highlights (TF-IDF test)

- **SUFFICIENT ↔ PARTIAL ↔ IRRELEVANT** dominate residual error (compositional substance/coverage).
- **CONTRADICTORY** remains easiest for bag-of-words (~0.93 F1) via failure lexemes in `ROW_DETAIL`.
- Exact matrices: `results/tfidf/metrics_test.json`.

## 5. Error analysis & Failure Lab

See `reports/ERROR_ANALYSIS.md` and `docs/failure-lab.html` (`docs/data/failure_lab.json` rebuilt from TF-IDF mistakes).

## 6. Limitations

Synthetic rule-derived labels; English-only; not a production auditor; Gemma conclusions reserved until GPU receipts exist. See `governance/LIMITATIONS.md` and `AI_RISK_REGISTER.md`.

## 7. Reproducibility

```bash
pip install -e ".[dev]"
python scripts/generate_dataset.py
python scripts/validate_dataset.py
python scripts/run_tfidf_baseline.py
python scripts/run_human_review.py
python scripts/build_failure_lab.py
python scripts/run_evaluation.py
python scripts/build_figures.py
python scripts/seal_protocol.py
pytest
```

GPU path: `notebooks/kaggle_runner.ipynb` / `KAGGLE_SAFE_RUN.md` — drop in HF token + Kaggle, write `results/gemma_*`, re-run `run_evaluation.py`.

## 8. Conclusion

At the classical stage, ControlSift’s main finding is methodological: a sealed, review-audited evidence benchmark can be made hard enough that TF-IDF no longer collapses the research question. Whether QLoRA recovers semantic headroom is the remaining empirical claim — and it waits on real GPU artifacts, not placeholders.
