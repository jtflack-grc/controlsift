# Changelog

## 1.2.0 — 2026-09-10

- Completed Gemma 3 1B zero-shot, few-shot, and QLoRA experiment path on dataset v1.0.0
- Preserved the controlled Gemma finding: few-shot outperformed QLoRA; QLoRA parse reliability was poor
- Published the dataset-version boundary: classical results use v1.1.0; Gemma results use v1.0.0; cross-version scores are descriptive only
- Finalized Failure Lab, Data/Model Cards, AI risk register, responsible-innovation material, and annotated external sources
- Finalized rubric-facing report and exactly eight presentation slides
- Completed and published the narrated capstone presentation as the `v1.0-capstone` GitHub Release asset
- Removed recording/teleprompter helpers and converted capstone status surfaces to complete
- Finalized submission package and career-facing project framing

## 1.1.0 — 2026-08-09

- Expanded footer-only MMC `/capstone/` hub: UN SDG/GFE alignment, DeepMind 8-course map, impact, methods, RAI, reflection, submission
- Dataset v1.1 compositional packet packing + AFLite-style surface harden (TF-IDF ~0.53 test)
- Protocol seal + git tag `protocol-v1-locked` (data/prompt contract; see `governance/TAGS.md`)
- Structural label audit + scripted 20-case spot-check (not human gold)
- Research surface decision disclosed (`governance/RESEARCH_SURFACE.md`)
- Front-door / portfolio / runway synced to the then-current classical-only status
- Safe Kaggle package path verified (`scripts/package_for_kaggle.py`)

At the 1.1.0 milestone, Gemma experiment metrics had not yet been executed; those runs were completed and published in the final capstone work recorded above.

## 1.0.0 — 2026-08-09

- Repository foundation, AGENTS.md, CI, configs
- Deterministic synthetic dataset engine (~1,500 cases) with family-level splits
- Dataset validation + leakage tests
- Majority and TF-IDF baselines with machine-readable results
- Protocol seal artifacts (`governance/PROTOCOL_SEAL.json`)
- Gemma zero/few-shot and QLoRA training/eval code paths (GPU environments)
- Evaluation: metrics, parser, slices, statistics, figures, learning curve
- Governance pack, research report, error analysis, Failure Lab
- Public GitHub Pages site + MMC capstone view + portfolio/resume bundle
