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

The capstone's problem and method are grounded in public sources including:

- NIST SP 800-53A Rev. 5 for control assessment and evidence-oriented verification
- NIST Small Business Cybersecurity resources for real-world cybersecurity resource constraints
- Dettmers et al., *QLoRA: Efficient Finetuning of Quantized LLMs*, for the fine-tuning method
- Google DeepMind's Gemma 3 documentation for model context
- NIST AI RMF for lifecycle risk, scope, oversight, and human-accountability boundaries
- United Nations SDG 10, Reduced Inequalities, for the official societal-goal mapping

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
