# ControlSift — execution runway (status)

**Charter path kept:** Gemma 3 1B IT + QLoRA, sealed protocol, Failure Lab, public receipts.

## Current position

| Item | Status |
|------|--------|
| Benchmark v1.1 + Gate 1 harden | **Done** (TF-IDF ~0.53 test) |
| Protocol tag `protocol-v1-locked` | **Done** |
| Classical baselines + public site | **Done** |
| Label audit (structural + scripted spot-check) | **Done** |
| Gemma zero-shot / few-shot / QLoRA TEST metrics | **Published** on Pages |
| GitHub Pages | **Live** — https://jtflack-grc.github.io/controlsift/ |
| ≤5-minute video | **Remaining** — record from `docs/capstone/video-script.html`; upload via GCLP form only |

Honest TEST takeaway: TF-IDF leads (~0.533); best Gemma ladder score is few-shot (~0.137); QLoRA (~0.083) with fragile label-parse success. Numbers from `results/*/metrics_test.json` only.

## Non-negotiables (rigor)

- No fabricated Gemma metrics
- No test-set prompt tuning after protocol seal
- Family-level split isolation stays enforced in CI
- Public site only shows machine-readable results
- HF token only in Kaggle/Colab Secrets — never in git
- Do not market v1.1 as naturalistic binder scoring (`governance/RESEARCH_SURFACE.md`)

## Reproduce (graders)

See [Reproduce](../reproduce.html) and `notebooks/KAGGLE_SAFE_RUN.md` in the repository (not published as a hub page). Published metrics remain on [Results](../results.html).

## Capstone bar

> I can determine whether domain adaptation actually improved a model, prove that result using controlled evidence, identify where it still fails, and explain where it should not be trusted.
