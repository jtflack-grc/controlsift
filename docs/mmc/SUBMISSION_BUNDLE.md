# MMC / GCLP Submission Package — ControlSift

Mentor Me Collective / Google Cloud Launchpad / DeepMind AI Research Foundations materials for ControlSift.

**Official UN SDG (GCLP required single selection):** Goal 10 — Reduced Inequalities.

> Handbook note: the live [GCLP Scholar Handbook](https://docs.google.com/document/d/1Peu87soSkTKkS0uUOaURF-jldbTg9XJJ8tZMzxojEWg) tabs were not machine-readable here (401). Requirements were reconciled against scholar copies of the **Capstone Project Outline** and **Capstone GitHub Project Structure**. Re-check the live Doc before form submit.

## Weekly DeepMind lab deliverables (Weeks 1–9)

| Path | Contents |
|------|----------|
| [`capstone/deliverables/`](../capstone/deliverables/index.html) | Hub for handbook weekly Key Deliverables |
| [`mmc/labs/`](../../mmc/labs/) | Runnable numpy labs (`python -m mmc.labs.run_all`) |
| [`mmc/deliverables/`](../../mmc/deliverables/) | Badge slot, alignment report, accelerate notes, outputs |

## Capstone pages

| Page | Contents |
|------|----------|
| [`gclp-checklist.html`](../capstone/gclp-checklist.html) | Outline + GitHub compliance matrix |
| [`report.html`](../capstone/report.html) | ≤8-page printable report |
| [`slides.html`](../capstone/slides.html) | Exactly 8 slides |
| [`video-script.html`](../capstone/video-script.html) | ≤5-minute script (record before upload) |
| [`implementation-plan.html`](../capstone/implementation-plan.html) | Phases, resources, risks |
| [`paper.html`](../capstone/paper.html) | Full research narrative |
| [`/capstone/`](../capstone/index.html) | Hub |
| [`un-sdg.html`](../capstone/un-sdg.html) | Official Goal 10 + context |
| [`curriculum.html`](../capstone/curriculum.html) | DeepMind subtopic map |
| [`problem-impact.html`](../capstone/problem-impact.html) | Problem, aim, stakeholders |
| [`methods-evidence.html`](../capstone/methods-evidence.html) | Dataset, ladder, evaluation |
| [`responsible-innovation.html`](../capstone/responsible-innovation.html) | Assurance documents |
| [`reflection.html`](../capstone/reflection.html) | Findings and next steps |
| [`submission.html`](../capstone/submission.html) | Reviewer package |

## GitHub structure (GCLP)

| Required | Location |
|----------|----------|
| README (problem, data, findings, tools, CRISP-DM) | `README.md` |
| requirements.txt | `requirements.txt` |
| data/raw + data/processed | `data/raw/`, `data/processed/` |
| notebooks | `notebooks/01_…`–`06_…` |
| reports/figures | `reports/figures/` |
| reflection | `reflection/project_reflection.md` |

## Reading order for evaluators

1. [`capstone/gclp-checklist.html`](../capstone/gclp-checklist.html)  
2. [`capstone/report.html`](../capstone/report.html) or [`paper.html`](../capstone/paper.html)  
3. Results + Failure Lab + Assurance  
4. Curriculum map  

## Evidence inventory

1. Dataset manifest hashes and `governance/PROTOCOL_SEAL.json`
2. Classical metrics (`results/majority/`, `results/tfidf/`)
3. Gemma / QLoRA metrics (`results/gemma_*`) when available
4. Failure Lab (`docs/data/failure_lab.json`)
5. Figures (`reports/figures/`)
6. Label audit (`data/review_log.csv`, audit reports)
7. Reflection files

## Still required of the scholar (not automatable here)

- Record ≤5-minute video  
- Export report/slides to PDF if the form requires files  
- Confirm live Handbook dates/form URL  
- Complete HF/Kaggle Gemma runs before claiming LLM outcomes  

## Acknowledgement

ControlSift was developed as an independent applied-AI research project following participation in Google DeepMind’s AI Research Foundations curriculum through Mentor Me Collective.
