# ControlSift

**Can a small AI model tell proof from paperwork?**

ControlSift is an applied AI assurance research project on cybersecurity control-evidence quality. It combines a synthetic benchmark, classical baselines, Gemma 3 experiments, failure analysis, governance artifacts, and a public research site.

> Status: **complete**. The research, report, eight-slide presentation, and narrated capstone video are finished. Classical experiments use dataset **v1.1.0**. Gemma zero-shot, few-shot, and QLoRA experiments were completed on dataset **v1.0.0** because of free-tier compute constraints. Cross-version scores are published for transparency but are **descriptive, not a controlled head-to-head comparison**.

## Why this matters

Cybersecurity and GRC teams routinely confuse *artifacts* with *proof*. A policy requiring MFA is not proof that MFA operated during the assessment period. An operational export can provide stronger evidence, and an export showing a failed control condition can contradict the control outright.

ControlSift asks whether a small language model can help classify evidence quality while preserving clear limits on what the experiment proves.

## Research question

Can parameter-efficient fine-tuning materially improve a small general-purpose language model's ability to evaluate the sufficiency and relevance of cybersecurity control evidence?

## Benchmark

Five classes:

- SUFFICIENT
- PARTIAL
- INSUFFICIENT
- IRRELEVANT
- CONTRADICTORY

Current hardened classical benchmark:

- approximately 1,500 synthetic cases
- train / validation / test / challenge: 1000 / 200 / 200 / 100
- scenario-family isolation across splits
- canonical seed: `42`
- dataset version: **1.1.0**

The Gemma experiments were run earlier against **v1.0.0**. Those results remain valid for within-version comparisons among Gemma zero-shot, few-shot, and QLoRA, but should not be treated as an apples-to-apples comparison with the v1.1 classical scores.

## Model ladder

```text
Classical v1.1: Majority -> TF-IDF + logistic regression
Gemma v1.0:     Zero-shot -> Few-shot -> QLoRA
```

Primary metric: **macro F1**.

## Published results

### Classical experiments - dataset v1.1.0

| Experiment | Test macro F1 | Challenge macro F1 |
|---|---:|---:|
| Majority | **0.0667** | 0.0667 |
| TF-IDF + logistic regression | **0.5327** | **0.5237** |

### Gemma experiments - dataset v1.0.0

| Experiment | Test macro F1 | Challenge macro F1 | Test parse success |
|---|---:|---:|---:|
| Gemma 3 1B zero-shot | **0.0796** | 0.1055 | 0.760 |
| Gemma 3 1B few-shot | **0.1365** | **0.1741** | 0.985 |
| Gemma 3 1B QLoRA | **0.0827** | 0.1309 | 0.435 |

Within the Gemma v1.0 ladder, **few-shot is the strongest run** and **QLoRA does not beat few-shot**. The low QLoRA parse-success rate is itself an important failure mode.

The v1.1 TF-IDF result and v1.0 Gemma results should **not** be used to claim that one model family definitively beat the other on the same benchmark. A controlled cross-family claim would require rerunning one side on the other's dataset version, which is outside the scope of this free-tier capstone.

Machine-readable sources live under `results/*/metrics_*.json` and feed `docs/data/results.json`.

## Research integrity

ControlSift deliberately keeps several boundaries visible:

- labels are rule-derived on synthetic data, not a large human gold standard
- test and challenge families are isolated from training families
- malformed model outputs count against performance
- metrics are published from result files rather than invented or hand-entered claims
- cross-version model comparisons are labeled descriptive rather than controlled
- the project is not a production auditor or compliance engine

An early generator allowed TF-IDF to saturate at 1.0. The benchmark was hardened before the v1.1 protocol seal so simple lexical shortcuts no longer defined a trivial task.

## External grounding

The capstone uses a diversified research base rather than relying on a single framework:

- **Evidence quality and assurance:** NIST SP 800-53A Rev. 5, PCAOB AS 1105, and The IIA Global Internal Audit Standards ground the distinction between document presence and evidence that is relevant, reliable, sufficient, and tied to an assessment objective.
- **AI and LLM use in adjacent domains:** Yang et al.'s systematic review of LLMs in cybersecurity and Kokina et al.'s field study of AI in auditing provide current research context on document-oriented AI use, evaluation challenges, reliability, explainability, governance, and overreliance.
- **Small-model and PEFT context:** Hu et al.'s *LoRA* paper, Dettmers et al.'s *QLoRA* paper, and Google DeepMind's Gemma 3 documentation ground the parameter-efficient adaptation method and lightweight model choice.
- **Responsible AI and human oversight:** NIST AI RMF 1.0 and EU AI Act Article 14 ground explicit scope, monitoring, human-AI roles, automation-bias awareness, and meaningful human override.

Small-business cybersecurity resource constraints and UN SDG 10 are retained separately as capstone-program context rather than treated as technical evidence. None of the external sources are used to claim that ControlSift works in production; project-specific performance claims come only from the committed experiment records.

Annotated source notes and claim boundaries: `docs/capstone/research-sources.html`.

## Explore

- [Public research site](docs/index.html)
- [Final narrated presentation](https://github.com/jtflack-grc/controlsift/releases/download/v1.0-capstone/ControlSift_Capstone_Slides.mp4)
- [Capstone release](https://github.com/jtflack-grc/controlsift/releases/tag/v1.0-capstone)
- [Results](docs/results.html)
- [Methods](docs/methods.html)
- [Failure Lab](docs/failure-lab.html)
- [Assurance](docs/assurance.html)
- [Reproduce](docs/reproduce.html)
- [Capstone hub](docs/capstone/index.html)
- [Research paper](docs/capstone/paper.html)
- [Capstone report](docs/capstone/report.html)
- [Research sources](docs/capstone/research-sources.html)

## Methodology

1. Deterministic synthetic evidence generation with rule-derived labels
2. Family-level split isolation and integrity tests
3. Classical baselines and lexical-ceiling hardening
4. Gemma 3 1B zero-shot and few-shot prompting
5. Gemma 3 1B QLoRA on free-tier GPU infrastructure
6. Held-out and challenge evaluation, error analysis, and failure inspection
7. Data Card, Model Card, intended-use limits, and AI risk register

## CRISP-DM mapping

| CRISP-DM step | ControlSift |
|---|---|
| Business understanding | Evidence-quality problem and MMC Goal 4 / UN SDG 10 framing |
| Data understanding | Dataset exploration, Data Card, scenario families |
| Data preparation | Generator, processed splits, validators, protocol seal |
| Modeling | Classical baseline, zero-shot, few-shot, QLoRA |
| Evaluation | Published metrics, Failure Lab, challenge sets, error analysis |
| Deployment | Out of scope; public research artifact only |

## Reproduction

```bash
python -m venv .venv
pip install -e ".[dev]"
python scripts/validate_dataset.py
python scripts/run_tfidf_baseline.py
pytest
```

Gemma training and inference used free Kaggle / Colab GPU paths. Tokens remain in platform secret stores and are never committed to git.

## Responsible use

ControlSift is **not** an automated auditor, compliance-certification engine, or replacement for human judgment. It is a bounded synthetic-benchmark research project.

## MMC / UN goal wording

For the capstone rubric, the project uses **MMC rubric option 4: Reduced Inequalities**. The official United Nations designation is **Sustainable Development Goal 10: Reduced Inequalities**.

## Acknowledgements

Independent applied research project developed in the Mentor Me Collective / Google DeepMind AI Research Foundations context.