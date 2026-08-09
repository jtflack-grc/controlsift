# Limitations

- **Synthetic data:** Generator assumptions may not match real audit evidence distributions.
- **Rule-derived labels:** Not a fully human-labeled gold standard; challenge set requires full review.
- **Lexical residual shortcuts:** Classical models can still perform strongly; interpret LLM gains carefully.
- **Single small model:** Results for Gemma 3 1B IT do not generalize to larger models or other families without further study.
- **No multi-artifact packages:** v1 cases are single evidence texts, not full evidence binders.
- **No live inference product:** Static research artifact only.
- **Parse failures:** Malformed model outputs become `UNPARSEABLE` and count against performance.
