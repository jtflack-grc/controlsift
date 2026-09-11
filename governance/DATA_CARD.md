# Data Card - ControlSift Benchmark

## Summary

Synthetic cybersecurity control-evidence benchmark for five-class evidence quality classification.

| Item | Value |
|------|-------|
| Version | 1.1.0 |
| Total cases | 1,500 |
| Splits | train 1000 / validation 200 / test 200 / challenge 100 |
| Seed | 42 |
| Generation | Deterministic rule-based (`synthetic_rule_based`) |
| Domains | 13 control domains |
| Research surface | Compositional evidence packets (see `RESEARCH_SURFACE.md`) |

## Motivation

Support research on whether PEFT improves small-LM judgment of evidence sufficiency/relevance on a **leakage-controlled synthetic** task - not to train a production auditor.

## Composition

Each case includes control statement, environment, evidence type, evidence text, label, failure tags, difficulty, scenario family id, and split.

**Labels:** SUFFICIENT, PARTIAL, INSUFFICIENT, IRRELEVANT, CONTRADICTORY (balanced).

**v1.1 packet shape:** dual sections (claim + near-domain distractor), substance pointer, `SCOPE` inventory/file_rows integers, `ROW_DETAIL`, and shared decoy lexicon. This is intentional compositional structure, not naturalistic binder OCR.

## Ground truth

Primary labels are **rule-derived** inside the generator via controlled mutations. They're **not** fully human-labeled.

Label audit:

- Structural integrity audit: 100% challenge + stratified ~10% development sample (`structural_auditor_v1`)
- Narrative spot-check: 20 challenge cases, 4 per label (`spotcheck_v1`)
- Tracked in `data/review_log.csv`

## Collection / generation

- Scenario families in `data/scenarios/scenario_families.yaml`
- Generator: `src/controlsift/data/generate.py`
- Family-level split'solation (no family crosses partitions)
- Synthetic orgs, systems, accounts, tickets only

## Preprocessing / splits

See `src/controlsift/data/split.py`. Integrity checks in `validate.py` and CI.

## Split hashes (protocol seal)

| Split | n | SHA-256 |
|-------|---|---------|
| train | 1000 | `53b5c057f80f6ae5bd26c63dc2a03c7de96641b73094b4b464ff80ab39438d99` |
| validation | 200 | `d14f9bbe0c7d567c12f1a4f1d624bd0e47b1d12d0a6a3d916f9c6b95692ceef8` |
| test | 200 | `7476a67ec679b4e0198709a4fb812be43d43364b78d525dacee4ab6c1dab31d1` |
| challenge | 100 | `735cd57b874ae29e54f74e99c512df0cc0039bc5e0bd85dbf4f21f882b057cfe` |

## Risks and limitations

- Synthetic-to-real gap is material.
- Classical CONTRADICTORY remains easier than SUFFICIENT/IRRELEVANT; macro F1 needs per-class context.
- Strong neural scores may reflect schema reading - disclose that.
- Must not be described as production audit evidence.

## Maintenance

Prefer not regenerating after `protocol-v1-locked` unless intentionally opening dataset v1.2+. Validate with `python scripts/validate_dataset.py`. Seal: `governance/PROTOCOL_SEAL.json`.
