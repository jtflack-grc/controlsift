# MMC Submission Bundle — ControlSift

Optional Mentor Me Collective / DeepMind AI Research Foundations handoff.
**Do not** invent a second technical project for MMC formatting. Point at existing artifacts.

## Branding rule

- Primary public identity: **ControlSift**
- MMC / curriculum material lives under **`/capstone/`** (footer-linked only)
- README does **not** open with “this is my MMC capstone”

Suggested acknowledgement (capstone / footer only):

> ControlSift was developed as an independent applied-AI research project following participation in Google DeepMind’s AI Research Foundations curriculum through Mentor Me Collective.

## Capstone cluster (HTML)

| Page | Purpose |
|------|---------|
| [`/capstone/`](../capstone/index.html) | Evaluator hub |
| [`un-sdg.html`](../capstone/un-sdg.html) | UN SDG / Global Futures (GFE) scope — primary SDG 16 |
| [`curriculum.html`](../capstone/curriculum.html) | 8-course DeepMind map |
| [`problem-impact.html`](../capstone/problem-impact.html) | Problem, aim, stakeholders, impact |
| [`methods-evidence.html`](../capstone/methods-evidence.html) | Dataset, ladder, evaluation pointers |
| [`responsible-innovation.html`](../capstone/responsible-innovation.html) | RAI / Assurance map |
| [`reflection.html`](../capstone/reflection.html) | What failed / pending / next |
| [`submission.html`](../capstone/submission.html) | This checklist as a page |

## Public research site

- Home, Failure Lab, Results, Methods, Assurance, Reproduce
- Machine-readable metrics: `docs/data/results.json` ← `results/*/metrics_*.json`

## Evidence checklist

1. Dataset manifest hashes + `governance/PROTOCOL_SEAL.json`
2. Classical baseline metrics (`results/majority/`, `results/tfidf/`)
3. Gemma / QLoRA metrics (`results/gemma_*`) — **null until HF/Kaggle**
4. Failure Lab (`docs/data/failure_lab.json`)
5. Figures (`reports/figures/`)
6. Label audit (`data/review_log.csv`, `reports/HUMAN_REVIEW_AUDIT.md`, `SPOTCHECK_20.md`)
7. Reflection (classical done; append LLM outcomes after GPU)
8. UN SDG mapping page (honest 16 / 9 / 4 — no climate theater)

## Reflection prompts (fill after Gemma)

- What did fine-tuning change versus prompting?
- Where does the model still fail (vs TF-IDF residuals)?
- Did the model learn packet schema rather than evidence judgment?
- Why synthetic evidence is not production proof
- How protocol lock protected research integrity

## If MMC wants slides

Deck spine: Problem → SDG 16 fit → Curriculum map → Methods → Classical results → RAI → Pending GPU → Reflection.  
Generate from `/capstone/` + Results — no new experiments for slides alone.
