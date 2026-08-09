# Human Review Audit

- Rows audited: **250**
- Status counts: `{'reviewed': 250}`
- Challenge reviewed OK: **100/100**
- Flagged ids: 0

## Method

Deterministic structural auditor (`scripts/run_human_review.py`) checks v1.1 packet invariants:
SCOPE integers vs label, substance/section packing, INSUFFICIENT hedges, CONTRADICTORY ROW_DETAIL cues.
This is an integrity review of rule-derived labels, not a fresh subjective relabel from scratch.
