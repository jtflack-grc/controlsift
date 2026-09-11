# ControlSift - execution runway (complete)

**Charter path completed:** Gemma 3 1B IT + QLoRA, sealed protocol, Failure Lab, public receipts, capstone report, eight-slide deck, and narrated final presentation.

## Final position

| Item | Status |
|------|--------|
| Benchmark v1.1 + Gate 1 harden | **Done** - TF-IDF ~0.53 test |
| Protocol tag `protocol-v1-locked` | **Done** |
| Classical baselines + public site | **Done** |
| Label audit (structural + scripted spot-check) | **Done** |
| Gemma zero-shot / few-shot / QLoRA metrics | **Done** - v1.0 receipts published |
| GitHub Pages | **Live** - https://jtflack-grc.github.io/controlsift/ |
| Eight-slide presentation | **Done** |
| Narrated capstone presentation | **Done** - https://github.com/jtflack-grc/controlsift/releases/tag/v1.0-capstone |

## Final research boundary

Classical experiments use dataset v1.1.0. Gemma zero-shot, few-shot, and QLoRA use dataset v1.0.0. Within Gemma v1.0, few-shot is strongest and QLoRA doesn't beat it. Cross-version scores are descriptive rather than a controlled same-benchmark leaderboard.

## Non-negotiables (rigor)

- No fabricated Gemma metrics
- No test-set prompt tuning after protocol seal
- Family-level split isolation stays enforced in CI
- Public site shows published result receipts
- HF token stays in platform secret stores - never in git
- Don't market v1.1 as naturalistic binder scoring (`governance/RESEARCH_SURFACE.md`)

## Reproduce

See [Reproduce](../reproduce.html) and `notebooks/KAGGLE_SAFE_RUN.md` in the repository. Published metrics remain on [Results](../results.html).

## Capstone bar

> I can evaluate whether domain adaptation improved a model, preserve a negative result when it didn't, identify where it fails, and explain where it shouldn't be trusted.
