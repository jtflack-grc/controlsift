# Agent Operating Rules — ControlSift

Non-negotiable instructions for humans and coding agents working in this repository.

## Research Integrity

- Never fabricate results.
- Never manufacture placeholder metrics that look like real scores.
- Never alter labels because the model disagrees.
- Never tune against the held-out test set.
- Never leak scenario families across partitions.
- Never describe synthetic evidence as production evidence.
- Never describe rule-derived labels as completely human-labeled.
- Preserve negative findings.

## Security

- Never commit secrets.
- Never commit employer data.
- Never commit Hugging Face tokens.
- Never commit Kaggle credentials.
- Never commit private evidence.
- Never commit production logs.

## Reproducibility

- Use fixed seeds where practical (canonical seed: `42`).
- Store configuration separately under `configs/`.
- Log dependency versions, hardware, dataset hashes, and model ID.
- Preserve raw predictions alongside metrics.

## Website

- No fabricated statistics. Public metrics must come from machine-readable `results/` files; use `null` until experiments run.
- No glowing AI robot imagery.
- Progressive disclosure.
- Main site optimized for public comprehension.
- Technical evidence remains accessible.

## Scope Discipline

Do not expand v1 into:

- SaaS
- live inference
- RAG
- agent workflows
- document ingestion
- OCR
- authentication
- production GRC software

## Source of truth

The master charter is `ControlSift.md`. Engineering layout follows Section 46. Phase gates in Section 62 govern when modeling and public claims may proceed.
