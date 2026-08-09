# Label Audit Protocol (Human Review Hub)

## Principles

- Do **not** describe the dataset as fully human-labeled.
- Rule-derived labels are primary.
- Distinguish **structural integrity audit** from **narrative spot-check** from **full human gold relabeling**.

## What has been done (v1.1 / protocol lock)

| Pass | Coverage | Reviewer id | What it checks |
|------|----------|-------------|----------------|
| Structural audit | 100% challenge + stratified ~10% dev sample | `structural_auditor_v1` | Packet invariants: `SCOPE` vs label, substance/section packing, INSUFFICIENT hedges, CONTRADICTORY `ROW_DETAIL` cues |
| Narrative spot-check | 20 challenge cases (4 per label) | `spotcheck_v1` | Case-specific reading notes; labels retained | 

Receipts: `data/review_log.csv`, `reports/HUMAN_REVIEW_AUDIT.md`, `reports/SPOTCHECK_20.md`.

## What this is not

- Not independent expert adjudication of every case
- Not authorization to claim “human-labeled gold”
- Not permission to edit sealed test labels after `protocol-v1-locked`

## Status values

| Status | Meaning |
|--------|---------|
| `unreviewed` | Not yet inspected |
| `reviewed` | Inspected; label retained |
| `corrected` | Label or text corrected after review |
| `flagged` | Audit found an invariant violation needing judgment |

When correcting, update both `review_log.csv` and the corresponding JSONL row; regenerate manifest hashes; prefer avoiding test-set edits after seal — open a new dataset version instead.
