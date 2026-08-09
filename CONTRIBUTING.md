# Contributing to ControlSift

ControlSift is a research integrity project. Contributions that improve rigor, reproducibility, or clarity are welcome. Contributions that expand scope into product features (SaaS, live inference, RAG, OCR, auth) are out of scope for v1.

## Research integrity

- Never fabricate results or placeholder metrics that look real.
- Never alter labels because a model disagrees.
- Never tune against the held-out test set.
- Never leak scenario families across train/validation/test/challenge.
- Preserve negative and mixed findings.

## Development setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## Pull requests

1. Keep changes focused.
2. Add or update tests for data integrity and parsers.
3. Ensure CI checks pass (schema, leakage, duplicates, metrics).
4. Do not commit secrets, credentials, or employer/customer data.

## GPU work

Train and run Gemma on Kaggle (or Colab fallback). Commit predictions, metrics, configs, and adapter metadata back to GitHub — not secrets or large weight blobs unless explicitly intended.
