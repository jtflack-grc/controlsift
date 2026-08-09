# Research Surface Decision — Dataset v1.1.0

**Decision (locked with protocol):** Keep the v1.1 compositional packet format. Do not silently market it as naturalistic binder prose.

## What v1.1 measures

Cases pack claim text and a near-domain distractor into dual sections, with shared decoy lexicon, identical `SCOPE` scaffolding, substance pointers, epistemic hedges, and `ROW_DETAIL` conflicts. Labels remain the five charter classes (SUFFICIENT → CONTRADICTORY).

The intended scientific claim after Gemma runs is:

> Can PEFT improve a small LM on **compositional evidence-packet reading** after lexical shortcuts are adversarially reduced?

It is **not** yet a claim about scoring raw customer PDF binders in production.

## Why this surface (not a corner)

| Risk if we pretend otherwise | Mitigation |
|------------------------------|------------|
| Overclaim “proof vs paperwork” on naturalistic evidence | State the compositional surface in README, Data Card, Limitations, site |
| Gemma “wins” by regex on `SCOPE` / section names | Report per-class + Failure Lab; treat schema-only wins as limited |
| TF-IDF AFLite overfits anti-bag-of-words | Ceiling test + honest classical receipts; neural gains still required |
| Prompt frozen without format tutorial | Zero-shot must discover packet grammar — that failure mode is a result |

## Non-goals for this lock

- Regenerating into freer prose before first Gemma baseline (would move seal hashes and reopen Gate 2)
- Changing the canonical prompt after `protocol-v1-locked`
- Claiming human gold labels for the full corpus

## If results show schema gaming

Document it. Optionally schedule a **v1.2 prose-hardened** follow-on with a new protocol tag — do not quietly relabel v1.1.
