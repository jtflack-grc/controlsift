# Changelog

## 1.1.0 — 2026-08-09

- Dataset v1.1 compositional packet packing + AFLite-style surface harden (TF-IDF ~0.53 test)
- Protocol seal + git tag `protocol-v1-locked` (data/prompt contract; see `governance/TAGS.md`)
- Structural label audit + scripted 20-case spot-check (not human gold)
- Research surface decision disclosed (`governance/RESEARCH_SURFACE.md`)
- Front-door / portfolio / runway synced to classical-only status
- Safe Kaggle package path verified (`scripts/package_for_kaggle.py`)

**Note:** Gemma experiment metric files remain `null` until executed on Kaggle/Colab.

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
