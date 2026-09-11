# MMC / GCLP Submission Package - ControlSift

Mentor Me Collective / Google Cloud Launchpad / DeepMind AI Research Foundations materials for the completed ControlSift capstone.

**MMC rubric option 4:** Reduced Inequalities.  
**Official UN designation:** Sustainable Development Goal 10 - Reduced Inequalities.

> Handbook note: the live GCLP Scholar Handbook wasn't machine-readable during project development. Requirements were reconciled against scholar copies of the Capstone Project Outline and Capstone GitHub Project Structure. The final artifact package is complete; confirm the live portal instructions when submitting administratively.

## Weekly DeepMind lab deliverables

| Path | Contents |
|------|----------|
| [`capstone/deliverables/`](../capstone/deliverables/index.html) | Hub for handbook weekly Key Deliverables |
| [`mmc/labs/`](../../mmc/labs/) | Runnable numpy labs (`python -m mmc.labs.run_all`) |
| [`mmc/deliverables/`](../../mmc/deliverables/) | Badge, alignment report, accelerate notes, outputs |

## Capstone pages and artifacts

| Page / artifact | Contents |
|------|----------|
| [`gclp-checklist.html`](../capstone/gclp-checklist.html) | Outline + GitHub compliance matrix |
| [`report.html`](../capstone/report.html) | Rubric-facing report |
| [`slides.html`](../capstone/slides.html) | Exactly 8 slides |
| [Final narrated presentation](https://github.com/jtflack-grc/controlsift/releases/download/v1.0-capstone/ControlSift_Capstone_Slides.mp4) | Completed ≤5-minute capstone presentation |
| [Final GitHub release](https://github.com/jtflack-grc/controlsift/releases/tag/v1.0-capstone) | `v1.0-capstone` release and presentation asset |
| [`implementation-plan.html`](../capstone/implementation-plan.html) | Phases, resources, risks |
| [`paper.html`](../capstone/paper.html) | Full research narrative |
| [`/capstone/`](../capstone/index.html) | Complete capstone hub |
| [`un-sdg.html`](../capstone/un-sdg.html) | MMC option 4 / official UN SDG 10 |
| [`curriculum.html`](../capstone/curriculum.html) | DeepMind curriculum map |
| [`problem-impact.html`](../capstone/problem-impact.html) | Problem, aim, stakeholders |
| [`methods-evidence.html`](../capstone/methods-evidence.html) | Dataset, model paths, evaluation |
| [`responsible-innovation.html`](../capstone/responsible-innovation.html) | Assurance documents |
| [`reflection.html`](../capstone/reflection.html) | Findings and learning reflection |
| [`submission.html`](../capstone/submission.html) | Form-ready package |

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
3. [Final narrated presentation](https://github.com/jtflack-grc/controlsift/releases/download/v1.0-capstone/ControlSift_Capstone_Slides.mp4)
4. Results + Failure Lab + Assurance
5. Curriculum map

## Evidence inventory

1. Dataset manifest hashes and `governance/PROTOCOL_SEAL.json`
2. Classical v1.1 metrics (`results/majority/`, `results/tfidf/`)
3. Gemma v1.0 zero-shot / few-shot / QLoRA metrics (`results/gemma_*`)
4. Failure Lab (`docs/data/failure_lab.json`)
5. Figures (`reports/figures/`)
6. Label audit (`data/review_log.csv`, audit reports)
7. Reflection files
8. Final report, PowerPoint, PDF slides, and narrated video

## Completion status

All project and rubric-facing artifacts are complete. A later upload through the MMC program portal is an administrative submission action, not unfinished project work.

## Acknowledgement

ControlSift was developed as an independent applied-AI research project following participation in Google DeepMind’s AI Research Foundations curriculum through Mentor Me Collective.
