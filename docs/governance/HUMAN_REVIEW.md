# Human Review Protocol

## Principles

- Do not describe the dataset as fully human-labeled.
- Rule-derived labels are primary; humans audit for generator defects and ambiguity.

## Development corpus (~10%)

Stratified across class, domain, difficulty, and major failure tags. Sample list is initialized in `data/review_log.csv` with `priority=dev_sample`.

## Challenge set (100%)

Every challenge case appears in `data/review_log.csv` with `priority=challenge_required`.

## Status values

| Status | Meaning |
|--------|---------|
| `unreviewed` | Not yet inspected |
| `reviewed` | Inspected; label retained |
| `corrected` | Label or text corrected after review |

When correcting, update both `review_log.csv` and the corresponding JSONL row; regenerate manifest hashes; document the change in the research report if post-protocol-lock (prefer avoiding test-set edits after seal).
