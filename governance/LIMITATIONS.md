# Limitations

- **Synthetic data:** Generator assumptions may not match real audit evidence distributions.
- **Rule-derived labels:** Not a fully human-labeled gold standard. Challenge coverage uses structural audit + a 20-case narrative spot-check — say that precisely.
- **Compositional research surface (v1.1):** Packets use dual sections, shared decoys, and explicit `SCOPE` / substance scaffolding. Strong model scores may reflect **schema reading**, not naturalistic binder judgment. See `governance/RESEARCH_SURFACE.md`.
- **Uneven class difficulty:** Classical CONTRADICTORY remains easier than SUFFICIENT / IRRELEVANT; interpret macro F1 with per-class tables.
- **Lexical residual / AFLite:** Surface forms were selected partly to reduce TF-IDF confidence; neural gains still need held-out proof.
- **Single small model:** Results for Gemma 3 1B IT do not generalize to larger models or other families without further study.
- **Frozen prompt:** Canonical zero-shot prompt does not tutor the packet grammar; discovery failures are valid outcomes.
- **No multi-artifact packages:** v1 cases are single evidence texts, not full evidence binders.
- **No live inference product:** Static research artifact only.
- **Parse failures:** Malformed model outputs become `UNPARSEABLE` and count against performance.
