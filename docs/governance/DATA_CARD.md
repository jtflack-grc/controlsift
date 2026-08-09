# Data Card — ControlSift Benchmark

## Summary

Synthetic cybersecurity control-evidence benchmark for five-class evidence quality classification.

| Item | Value |
|------|-------|
| Version | 1.1.0 |
| Total cases | ~1,500 |
| Splits | train 1000 / validation 200 / test 200 / challenge 100 |
| Seed | 42 |
| Generation | Deterministic rule-based (`synthetic_rule_based`) |
| Domains | ≥10 control domains |

## Motivation

Support research on whether PEFT improves small-LM judgment of evidence sufficiency/relevance — not to train a production auditor.

## Composition

Each case includes control statement, environment, evidence type, evidence text, label, failure tags, difficulty, scenario family id, and split.

**Labels:** SUFFICIENT, PARTIAL, INSUFFICIENT, IRRELEVANT, CONTRADICTORY (balanced).

## Ground truth

Primary labels are **rule-derived** inside the generator via controlled mutations. They are **not** fully human-labeled.

Human review:

- ~10% stratified sample of the development corpus
- **100%** of the challenge set expected
- Tracked in `data/review_log.csv` (`unreviewed` / `reviewed` / `corrected`)

## Collection / generation

- Scenario families in `data/scenarios/scenario_families.yaml`
- Generator: `src/controlsift/data/generate.py`
- Family-level split isolation (no family crosses partitions)
- Synthetic orgs, systems, accounts, tickets only

## Preprocessing / splits

See `src/controlsift/data/split.py`. Integrity checks in `validate.py` and CI.

## Risks and limitations

- Synthetic-to-real gap is material.
- Lexical baselines can still be strong; TF-IDF is used as a shortcut detector.
- Rule-derived labels may encode generator assumptions.
- Must not be described as production audit evidence.

## Maintenance

Regenerate with `python scripts/generate_dataset.py` and validate with `python scripts/validate_dataset.py`. Protocol seal hashes live in `governance/PROTOCOL_SEAL.json`.
