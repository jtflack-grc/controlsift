# Error Analysis — ControlSift

## Scope and version boundary

ControlSift has two completed experiment families that must remain separate in interpretation:

- Classical baselines use dataset **v1.1.0**.
- Gemma zero-shot, few-shot, and QLoRA use dataset **v1.0.0**.

Within-version conclusions are controlled. Cross-version scores are published for transparency but are descriptive, not a same-benchmark classical-vs-Gemma leaderboard.

## Classical baseline — dataset v1.1.0

| Split | TF-IDF macro F1 |
|-------|------------------|
| Validation | ~0.51 |
| Test | ~0.53 |
| Challenge | ~0.52 |

Earlier generator drafts saturated at macro F1 = 1.0 because label-unique lexical cues made the task trivial. Dataset v1.1 hardened the benchmark with dual-section packing, shared decoy lexicons, identical `SCOPE` scaffolding, and synonym selection against a train TF-IDF probe. The resulting ~0.53 test macro F1 is evidence that the original shortcut was materially reduced, not proof that all lexical shortcuts were eliminated.

### Per-class TF-IDF pattern on v1.1 test

| Label | Approx. F1 | Reading |
|-------|------------|---------|
| CONTRADICTORY | ~0.93 | Failure tokens in `ROW_DETAIL` remain comparatively recoverable |
| INSUFFICIENT | ~0.61 | Epistemic hedges retain some lexical signal |
| PARTIAL | ~0.52 | Often requires inventory vs. `file_rows` comparison |
| IRRELEVANT | ~0.35 | Depends more heavily on section composition and substance pointers |
| SUFFICIENT | ~0.25 | Collides with PARTIAL and IRRELEVANT lexical patterns |

Exact classical receipt: `results/tfidf/metrics_test.json`.

The balanced five-class majority baseline produces **accuracy 0.20** but **macro F1 about 0.067**. Public reporting uses the committed metrics rather than confusing accuracy with macro F1.

## Gemma experiments — dataset v1.0.0

| Experiment | Test macro F1 | Test parse success |
|------------|---------------|--------------------|
| Zero-shot | ~0.080 | ~0.760 |
| Few-shot | ~0.137 | ~0.985 |
| QLoRA | ~0.083 | ~0.435 |

Within the controlled Gemma v1.0 experiments, **few-shot prompting is strongest**. QLoRA does not beat few-shot and introduces a substantial output-contract failure: fewer than half of test responses parse into a valid target label. That formatting reliability issue is treated as part of model performance rather than silently repaired away.

The small numeric difference between zero-shot and QLoRA is not presented as a meaningful fine-tuning gain. The stronger conclusion is that the attempted QLoRA adaptation did not improve on few-shot prompting and materially worsened label-output reliability.

## Failure patterns

The project tracks several hard boundaries that aggregate macro F1 can hide:

1. **SUFFICIENT vs PARTIAL** — whether the evidence fully covers the claimed population or only part of it.
2. **SUFFICIENT vs IRRELEVANT** — whether a plausible artifact actually supports the control under review.
3. **INSUFFICIENT vs SUFFICIENT** — stated intent or weak narrative versus observed operational evidence.
4. **CONTRADICTORY vs SUFFICIENT** — evidence content that conflicts with the claimed control state.
5. **UNPARSEABLE model output** — especially important in the QLoRA run, where output-contract failure itself became a result.

`scripts/build_failure_lab.py` and the public Failure Lab preserve representative mistakes and difficult slices. `scripts/run_human_review.py` provides structural review receipts for the synthetic challenge data; this is not represented as an independently human-labeled gold standard.

## Research conclusion

The error analysis supports a bounded conclusion rather than a winner-takes-all leaderboard. Dataset hardening exposed how easily a synthetic benchmark can reward shortcuts. The completed Gemma runs showed that fine-tuning did not automatically improve classification and that output reliability can dominate usefulness. The dataset-version mismatch discovered during final review is explicitly retained as a reproducibility limitation instead of being hidden by an unsupported cross-family comparison.
