# Research Surface Decision — Dataset v1.1.0

**Decision (locked with protocol):** Keep the v1.1 compositional packet format. Do not silently market it as naturalistic binder prose.

## What v1.1 measures

Cases pack claim text and a near-domain distractor into dual sections, with shared decoy lexicon, identical `SCOPE` scaffolding, substance pointers, epistemic hedges, and `ROW_DETAIL` conflicts. Labels remain the five charter classes (SUFFICIENT → CONTRADICTORY).

The hardened v1.1 surface supports this research question:

> Can a model classify **compositional evidence packets** after obvious lexical shortcuts are adversarially reduced?

The completed classical experiments answer part of that question on v1.1.0. The completed Gemma zero-shot, few-shot, and QLoRA experiments were run on v1.0.0, so they do **not** establish how PEFT performs on the hardened v1.1 surface. Within the controlled Gemma v1.0 experiments, few-shot prompting is strongest and QLoRA does not beat it. Cross-version scores are descriptive only.

This is **not** a claim about scoring raw customer PDF binders in production.

## Why this surface (not a corner)

| Risk if we pretend otherwise | Mitigation |
|------------------------------|------------|
| Overclaim “proof vs paperwork” on naturalistic evidence | State the compositional surface in README, Data Card, Limitations, site |
| A model “wins” by schema cues such as `SCOPE` / section names | Report per-class + Failure Lab; treat schema-only wins as limited |
| TF-IDF AFLite overfits anti-bag-of-words | Ceiling test + honest classical receipts; do not infer neural gains from cross-version scores |
| Prompt format creates output-contract failure | Preserve parse reliability and unparseable outputs as part of evaluation |

## Non-goals for this lock

- Regenerating into freer prose after the protocol seal without a new dataset/version boundary
- Changing the canonical prompt after `protocol-v1-locked`
- Claiming human gold labels for the full corpus
- Presenting v1.1 classical and v1.0 Gemma scores as a controlled same-benchmark ranking

## Future research

A future v1.2 or later study could use freer prose, one common dataset version across all model families, stronger constrained decoding, and independent human review. Any such extension should receive a new protocol tag rather than silently changing the completed capstone evidence trail.
