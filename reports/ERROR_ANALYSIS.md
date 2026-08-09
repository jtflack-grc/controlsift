# Error Analysis — ControlSift (dataset v1.1.0)

## Scope

Classical baseline errors on the sealed test/challenge sets after compositional hardening. LLM-specific analysis is appended only after Gemma artifacts land in `results/`.

## TF-IDF baseline (Gate 1, post-harden)

| Split | Macro F1 |
|-------|----------|
| Validation | ~0.51 |
| Test | ~0.53 |
| Challenge | ~0.52 |

Earlier generator drafts saturated at macro F1 = 1.0 (label-unique cue phrases). v1.1 uses dual-section packing, shared decoy lexicons, identical `SCOPE` scaffolding, and AFLite-style synonym selection against a train TF-IDF probe. Lexical shortcuts are no longer sufficient for a strong overall score.

### Per-class (test)

| Label | Approx. F1 | Reading |
|-------|------------|---------|
| CONTRADICTORY | ~0.93 | Still helped by failure tokens inside `ROW_DETAIL` |
| INSUFFICIENT | ~0.61 | Epistemic hedges partially recoverable |
| PARTIAL | ~0.52 | Needs inventory vs `file_rows` comparison |
| IRRELEVANT | ~0.35 | Substance-pointer / section composition |
| SUFFICIENT | ~0.25 | Collides with PARTIAL and IRRELEVANT bags |

### Confusion patterns to watch for Gemma

1. **SUFFICIENT ↔ PARTIAL** — equal vs unequal `SCOPE` integers with shared claim text  
2. **SUFFICIENT ↔ IRRELEVANT** — same token multiset risk when distractor and claim co-occur  
3. **INSUFFICIENT ↔ SUFFICIENT** — hedges vs observed operational reading  
4. **CONTRADICTORY ↔ SUFFICIENT** — whether models read `ROW_DETAIL` against the control  

Exact matrix: `results/tfidf/metrics_test.json`.

## Majority baseline receipt

Balanced 5-class majority yields **accuracy 0.20** but **macro F1 ≈ 0.067** (not 0.20). Public copy and the research report use the metrics JSON values, not accuracy-as-F1.

## Failure Lab

`scripts/build_failure_lab.py` selects TF-IDF test mistakes (stratified) plus challenge hard-tag fills into `docs/data/failure_lab.json`. Gemma prediction slots stay `null` until GPU runs.

## Human review

`scripts/run_human_review.py` structurally audits every challenge row and the stratified sample. Receipt: `reports/HUMAN_REVIEW_AUDIT.md`. Flagged rows block an “all-clear” audit (`ok: false`).

## Next updates (post-GPU)

- Parse-failure (`UNPARSEABLE`) gallery  
- Zero-shot vs QLoRA confusion deltas  
- Slice tables by `failure_tags` / domain for the adapted model  
