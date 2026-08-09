# ControlSift — 12-Week Runway (Original Path)

**Decision:** Stay with the charter path — Gemma 3 1B IT + QLoRA, sealed protocol, Failure Lab, public receipts.  
**Do not** swap to a weaker “classical-only capstone” framing unless accounts become permanently impossible.

## Current position (updated)

| Item | Status |
|------|--------|
| Benchmark v1.1 + Gate 1 harden | **Done** (TF-IDF ~0.53 test) |
| Protocol tag `protocol-v1-locked` | **Done** (seals dataset/prompt; see `governance/TAGS.md`) |
| Classical baselines + public site | **Done** |
| Label audit (structural + scripted spot-check) | **Done** |
| Front-door / portfolio honesty sync | **Done** |
| HF + Kaggle accounts / Gemma metrics | **Blocked** — your next action |
| Remote GitHub + Pages URL | Optional whenever you create the remote |

Remaining calendar: still ~**12 weeks** of modeling + writeup once GPU access exists; classical scaffolding is no longer the bottleneck.

## Non-negotiables (rigor)

- No fabricated Gemma metrics
- No test-set prompt tuning after protocol seal
- Family-level split isolation stays enforced in CI
- Public site only shows machine-readable results
- HF token only in Kaggle/Colab Secrets — never in git
- Do not market v1.1 as naturalistic binder scoring (`governance/RESEARCH_SURFACE.md`)

## Week map (from GPU day = week 1)

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
| **9** | Site polish | Home/Results/Failure Lab show real Gemma numbers |
| **10** | Capstone page | `/capstone/` complete; MMC bundle checklist green |
| **11** | Hardening | CI green; secret scan; optional prose-hardened v1.2 plan if schema gaming dominates |
| **12** | Release | Tag `v1.0.0` science release (protocol tag already exists); README/portfolio final |

Slip buffer: weeks 9–12 absorb GPU quota delays.

## Critical path (do now)

1. Create **Hugging Face** + **Kaggle** (free).  
2. Accept Gemma license; store **read** token as Kaggle Secret `HF_TOKEN`.  
3. Regenerate/upload `dist/controlsift_kaggle_bundle.zip` via `python scripts/package_for_kaggle.py`.  
4. Run [`notebooks/kaggle_runner.ipynb`](../notebooks/kaggle_runner.ipynb) with `SMOKE=True`, then `False`.  
5. Merge outputs → `python scripts/run_evaluation.py` → `python scripts/build_figures.py`.

## Already secured in-repo

- Benchmark + leakage tests + lexical ceiling test  
- Protocol seal + tag; research-surface decision recorded  
- Classical ladder (majority 0.067 / TF-IDF ~0.53)  
- Structural audit + scripted 20-case spot-check (not human gold)  
- Safe GPU packaging/runner (no secrets in tree)  
- Public site + governance + portfolio copy aligned to classical-only status  

## Capstone bar (original north star)

> I can determine whether domain adaptation actually improved a model, prove that result using controlled evidence, identify where it still fails, and explain where it should not be trusted.
