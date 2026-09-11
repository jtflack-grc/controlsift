# Phase Gate Status

| Gate | Name | Status | Evidence |
|------|------|--------|----------|
| 1 | Dataset Validity | **Passed** | Schema/balance/leakage; hardened v1.1 TF-IDF ~0.53 test / ~0.52 challenge |
| 2 | Protocol Lock | **Passed** | Tag `protocol-v1-locked` seals data/prompt; research boundary documented in `governance/TAGS.md` |
| 3 | Model Training | **Complete** | Gemma zero-shot / few-shot / QLoRA v1.0 metrics and predictions published under `results/gemma_*` |
| 4 | Evaluation & RAI | **Complete** | Classical + Gemma version-scoped evaluation, structural audit, spot-check, Failure Lab, Data/Model Cards, risk register |
| 5 | Public Release | **Complete** | [GitHub Pages](https://jtflack-grc.github.io/controlsift/) live; report, 8-slide deck, narrated presentation, and [`v1.0-capstone`](https://github.com/jtflack-grc/controlsift/releases/tag/v1.0-capstone) release published |

## Final interpretation

Classical experiments use dataset v1.1.0 and Gemma experiments use dataset v1.0.0. Within Gemma v1.0, few-shot is strongest and QLoRA does not beat it. Cross-version scores are published for transparency but are not presented as a controlled same-benchmark leaderboard.
