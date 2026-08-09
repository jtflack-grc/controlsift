# ControlSift Research Protocol (Locked Candidate)

**Tag target:** `protocol-v1-locked`  
**Dataset version:** 1.1.0  
**Canonical seed:** 42  
**Primary metric:** macro F1  
**Primary model:** `google/gemma-3-1b-it`  
**Adaptation:** QLoRA (4-bit NF4, LoRA r=16, α=16)

## Hypotheses (frozen)

- **H1:** QLoRA-adapted Gemma 3 1B achieves higher held-out macro F1 than the same model with a fixed zero-shot prompt.
- **H2:** QLoRA outperforms a fixed five-class few-shot prompt.
- **H3:** Measurable improvement remains on the challenge set (unseen families / harder defects).
- **H4:** Performance increases with training-set size with diminishing returns.
- **H5:** Difficult boundaries remain, especially PARTIAL↔INSUFFICIENT / PARTIAL↔SUFFICIENT / INSUFFICIENT↔IRRELEVANT / CONTRADICTORY↔PARTIAL.

Negative or mixed findings remain valid.

## Class definitions

Frozen per charter §12: SUFFICIENT, PARTIAL, INSUFFICIENT, IRRELEVANT, CONTRADICTORY.

## Prompt

Canonical zero-shot prompt is implemented in `src/controlsift/prompting/templates.py` (`ZERO_SHOT_TEMPLATE`).  
Few-shot uses one fixed representative example per class selected from train+validation only.

After this protocol is tagged, do **not** change the prompt based on held-out test failures.

## Evaluation procedure

1. Deterministic inference (`do_sample=false`, temperature 0 where supported).
2. Parse with `controlsift.evaluation.parser.parse_model_output`; ambiguous → `UNPARSEABLE`.
3. Report macro F1 primary; accuracy, macro P/R, per-class, confusion matrices, parse-success.
4. Bootstrap CIs; McNemar for paired model comparisons where appropriate.
5. Slice by control_domain, evidence_type, difficulty, failure_tags.
6. Evaluate sealed test and challenge splits only after Gate 3.

## Test-set seal

Generate `data/manifests/dataset_manifest.json` SHA-256 hashes for all splits.  
The test split hash at protocol lock is the research contract.

## Gate 1 note (pre-lock)

TF-IDF + logistic regression is intentionally strong on this synthetic benchmark after minimal-edit mutations, but no longer saturates at 1.0. Extremely high lexical scores were treated as a dataset-quality warning and addressed before lock. See `results/tfidf/gate1_lexical_note.json`.
