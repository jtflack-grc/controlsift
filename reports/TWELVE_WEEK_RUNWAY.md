# ControlSift — 12-Week Runway (Completed Early)

This file preserves the original execution plan as a retrospective. The planned 12-week path was completed early: classical baselines, Gemma prompting, QLoRA, failure analysis, governance artifacts, report, slides, narrated presentation, public site, and final capstone release are all complete.

## Final position

| Item | Status |
|------|--------|
| Benchmark v1.1 + Gate 1 harden | **Done** — TF-IDF ~0.53 test |
| Protocol tag `protocol-v1-locked` | **Done** |
| Classical baselines + public site | **Done** |
| Label audit (structural + scripted spot-check) | **Done** |
| Gemma zero-shot / few-shot / QLoRA | **Done** — dataset v1.0 receipts published |
| Error analysis + Failure Lab | **Done** |
| Governance / assurance refresh | **Done** |
| Research report + rubric-facing report | **Done** |
| Eight-slide presentation | **Done** |
| Narrated capstone presentation | **Done** — `v1.0-capstone` release |
| GitHub Pages | **Live** |

## Research-integrity boundary

- Classical majority and TF-IDF results use dataset v1.1.0.
- Gemma zero-shot, few-shot, and QLoRA results use dataset v1.0.0.
- Within Gemma v1.0, few-shot is the strongest run; QLoRA does not beat it.
- Cross-version classical-vs-Gemma scores are descriptive, not a controlled same-benchmark leaderboard.
- No fabricated metrics, post-seal test prompt tuning, or production-auditor claims.

## What the original runway accomplished

The original sequence was: establish the benchmark, lock the protocol, run classical baselines, obtain free-tier GPU access, execute Gemma zero-shot / few-shot / QLoRA, analyze failures, refresh governance artifacts, publish the research site, and package the capstone. That sequence is complete.

## Final capstone bar

> I can evaluate whether domain adaptation improved a model, preserve a negative result when it did not, identify failure modes, show the evidence behind the conclusion, and explain where the model should not be trusted.

Final release: https://github.com/jtflack-grc/controlsift/releases/tag/v1.0-capstone
