# ControlSift — 12-Week Runway (Original Path)

**Decision:** Stay with the charter path — Gemma 3 1B IT + QLoRA, sealed protocol, Failure Lab, public receipts.  
**Do not** swap to a weaker “classical-only capstone” framing unless accounts become permanently impossible.

Session so far (~1 hour): foundation, benchmark, classical baselines, site, governance, safe Kaggle runner.  
Remaining calendar: **~12 weeks** — comfortable if GPU access is obtained early.

## Non-negotiables (rigor)

- No fabricated Gemma metrics
- No test-set prompt tuning after protocol seal
- Family-level split isolation stays enforced in CI
- Public site only shows machine-readable results
- HF token only in Kaggle/Colab Secrets — never in git

## Week map

| Weeks | Focus | Exit criteria |
|-------|--------|----------------|
| **1** | Accounts + smoke | HF license accepted; Kaggle GPU notebook; `SMOKE=True` runner finishes; download zip merges locally |
| **2** | Full baselines | Zero-shot + few-shot on validation/test/challenge; metrics committed |
| **3** | QLoRA train | Full train (not smoke); adapter reloads; training_meta saved |
| **4** | QLoRA eval + Gate 3 | Test + challenge metrics for `gemma_qlora`; parser healthy |
| **5** | Statistics & slices | Bootstrap/McNemar vs baselines; slice tables; figures refreshed |
| **6** | Error analysis | Failure Lab updated with LLM misses; ERROR_ANALYSIS.md expanded |
| **7** | Governance refresh | Data/Model cards + risk register reflect real outcomes (incl. negatives) |
| **8** | Research report | RESEARCH_REPORT.md answers H1–H5 with uncertainty language |
| **9** | Site polish | Home/Results/Failure Lab show real numbers; no pending Gemma rows |
| **10** | Capstone page | `/capstone/` complete; MMC bundle checklist green |
| **11** | Hardening | Human review log advanced (challenge 100%); CI green; secret scan |
| **12** | Release | Tag `protocol-v1-locked` (if not already), `v1.0.0`; README/portfolio final |

Slip buffer is built in: weeks 9–12 can absorb GPU quota delays.

## Critical path (do early)

1. Create **Hugging Face** + **Kaggle** (free).  
2. Accept Gemma license; store **read** token as Kaggle Secret `HF_TOKEN`.  
3. Upload `dist/controlsift_kaggle_bundle.zip` (or regenerate via `python scripts/package_for_kaggle.py`).  
4. Run [`notebooks/kaggle_runner.ipynb`](../notebooks/kaggle_runner.ipynb) with `SMOKE=True`, then `False`.  
5. Merge outputs → `python scripts/run_evaluation.py`.

Until step 1–2 happen, modeling gates stay blocked — everything else can still advance (review log, site copy, report drafts with “pending GPU” sections).

## Already secured in-repo

- Benchmark + leakage tests  
- Protocol seal artifacts  
- Classical ladder + Gate 1 lexical hardening  
- Safe GPU packaging/runner (no secrets in tree)  
- Public site shell + governance stubs  
- Evaluation/figure pipelines ready for real JSON  

## Capstone bar (original north star)

By week 12 the artifact should support:

> I can determine whether domain adaptation actually improved a model, prove that result using controlled evidence, identify where it still fails, and explain where it should not be trusted.
