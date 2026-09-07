# Phase Gate Status

| Gate | Name | Status | Evidence |
|------|------|--------|----------|
| 1 | Dataset Validity | **Passed** | Schema/balance/leakage; TF-IDF uncomfortable (~0.53 test / ~0.52 challenge) |
| 2 | Protocol Lock | **Passed** | Tag `protocol-v1-locked` seals data/prompt; HEAD may advance docs (`governance/TAGS.md`) |
| 3 | Model Training | **Complete** | Gemma zero-shot / few-shot / QLoRA TEST metrics in `results/gemma_*` and `docs/data/results.json` |
| 4 | Evaluation & RAI | **Complete** | Classical + Gemma ladder on sealed TEST; structural audit + spot-check + Failure Lab |
| 5 | Public release | **Pages live** | [GitHub Pages](https://jtflack-grc.github.io/controlsift/) serves `docs/` with published TEST metrics |

Remaining submit step: record the ≤5-minute video from `docs/capstone/video-script.html` and upload via the GCLP form (do not commit the video).
