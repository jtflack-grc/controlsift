# ControlSift
## Applied AI Research, Model Assurance, and Cybersecurity Evidence Evaluation

### Master Project Charter, Research Protocol, Engineering Specification, Public Experience Plan, and Capstone Handoff

**Working project name:** ControlSift  
**Working public question:** *Can a small AI model tell proof from paperwork?*  
**Technical subtitle:** *Domain Adaptation of Gemma 3 for Cybersecurity Control-Evidence Assessment*  
**Status:** Pre-kickoff / independent development  
**Target:** Public v1.0 within approximately four months, subject to the official Mentor Me Collective schedule  
**Primary home:** GitHub  
**Public presentation:** GitHub Pages  
**Primary GPU environment:** Kaggle, with Google Colab as fallback  
**Primary model:** Gemma 3 1B instruction-tuned  
**Fine-tuning method:** QLoRA  
**Primary evaluation metric:** Macro F1

---

# 1. Executive Summary

ControlSift is an independent applied-AI research project investigating whether parameter-efficient fine-tuning can improve a small language model's ability to distinguish strong cybersecurity control evidence from artifacts that are incomplete, irrelevant, misleading, stale, or directly contradictory.

The research will compare several approaches against the same controlled benchmark:

1. Majority-class baseline
2. Traditional TF-IDF + logistic regression classifier
3. Gemma 3 1B zero-shot
4. Gemma 3 1B few-shot
5. Gemma 3 1B adapted using QLoRA

The project will create a synthetic cybersecurity control-evidence benchmark containing approximately 1,500 cases across five evidence-quality classes:

- SUFFICIENT
- PARTIAL
- INSUFFICIENT
- IRRELEVANT
- CONTRADICTORY

The project will deliberately emphasize experimental rigor rather than feature count.

It will include:

- a defined research question;
- explicit hypotheses;
- deterministic dataset generation;
- documented labeling rules;
- scenario-family split isolation;
- a frozen held-out test set;
- a separate challenge set;
- classical and LLM baselines;
- Gemma 3 QLoRA adaptation;
- training monitoring;
- quantitative evaluation;
- statistical comparison;
- slice-based performance analysis;
- error analysis;
- Data Card;
- Model Card;
- AI risk register;
- research report;
- public research site;
- reproducible source code;
- machine-readable results;
- automated integrity checks;
- a dedicated MMC capstone view;
- portfolio and resume integration.

The finished product must stand on its own regardless of Mentor Me Collective.

MMC may receive ControlSift as an optional capstone.

Google DeepMind's AI Research Foundations curriculum may provide the educational context.

Neither becomes the identity of the public project.

---

# 2. North Star

The project must ultimately demonstrate something more sophisticated than:

> I learned how to fine-tune Gemma.

The finished artifact should demonstrate:

> **I can determine whether domain adaptation actually improved a model, prove that result using controlled evidence, identify where the model still fails, and explain where it should not be trusted.**

This distinction governs the entire project.

ControlSift is as much an AI-assurance project as it is a fine-tuning project.

---

# 3. Why This Project Exists

Cybersecurity and GRC teams routinely receive evidence such as:

- screenshots;
- configuration exports;
- policies;
- IAM reports;
- SIEM output;
- change tickets;
- logs;
- vulnerability reports;
- backup reports;
- approval records;
- self-attestations.

Artifacts are frequently mistaken for proof merely because they are relevant to a control.

Examples:

A policy requiring MFA does not prove MFA is enabled.

A screenshot without scope or date may not establish operation during the audit period.

An IAM export showing one privileged user without MFA does more than fail to prove the control. It contradicts the control requirement.

A report covering eighteen of twenty accounts may demonstrate partial control operation without demonstrating the full population.

Humans make these distinctions using contextual judgment.

The research question is whether a small general-purpose language model can learn useful portions of that judgment through targeted domain adaptation.

---

# 4. Research Question

Primary research question:

> **Can parameter-efficient fine-tuning materially improve a small general-purpose language model's ability to evaluate the sufficiency and relevance of cybersecurity control evidence?**

Secondary questions:

1. Which evidence classes benefit most from fine-tuning?

2. Which evidence defects remain difficult after adaptation?

3. How does QLoRA adaptation compare with zero-shot and few-shot prompting?

4. How does the adapted model compare with a conventional lexical classifier?

5. How much specialized training data is required before improvement begins to plateau?

6. Does the adapted model generalize to scenario families intentionally withheld from training?

7. Does fine-tuning introduce new failure modes while correcting old ones?

8. Which evidence-quality boundaries remain most ambiguous?

---

# 5. Hypotheses

## H1: Domain Adaptation

Gemma 3 1B adapted using QLoRA will achieve higher held-out macro F1 than the same base model using a fixed zero-shot prompt.

## H2: Prompting Versus Fine-Tuning

QLoRA adaptation will outperform a fixed few-shot prompt containing representative examples of all five evidence classes.

## H3: Domain Generalization

The adapted model will retain measurable improvement on a separately constructed challenge set containing unseen scenario families, different wording patterns, and more complex evidence defects.

## H4: Data Scaling

Performance will increase as training-set size increases, but marginal improvement will eventually diminish.

## H5: Remaining Weaknesses

Fine-tuning will not eliminate all difficult semantic boundaries, particularly:

- PARTIAL versus INSUFFICIENT;
- PARTIAL versus SUFFICIENT;
- INSUFFICIENT versus IRRELEVANT;
- CONTRADICTORY versus PARTIAL.

These are hypotheses.

They are not promised outcomes.

Negative, mixed, or counterintuitive findings remain valid research results.

---

# 6. What ControlSift Is Not

ControlSift must never be represented as:

- an automated auditor;
- an autonomous GRC platform;
- a compliance-certification engine;
- a regulatory decision system;
- a replacement for control owners;
- a replacement for auditors;
- proof that LLMs can determine compliance;
- a production-ready evidence-review product.

ControlSift is:

> **A bounded research benchmark investigating domain adaptation for cybersecurity evidence assessment.**

That boundary is central to the responsible-AI story.

---

# 7. Audience Architecture

ControlSift serves four audiences.

## Audience A: Recruiter, Manager, General Visitor

Question:

> Why should I care?

They need:

- a problem understandable within seconds;
- one strong example;
- three headline numbers;
- before-versus-after behavior;
- visible failures;
- a clear explanation of why the experiment matters.

Time budget:

**60 to 90 seconds.**

## Audience B: GRC / Cybersecurity Practitioner

Question:

> Does this reflect how evidence actually works?

They need:

- realistic evidence pathologies;
- control examples;
- Failure Lab;
- limitations;
- evidence-quality taxonomy;
- responsible-use framing.

Time budget:

**5 to 10 minutes.**

## Audience C: ML / Technical / Research Reviewer

Question:

> Prove the experiment is legitimate.

They need:

- research protocol;
- split methodology;
- baseline ladder;
- hyperparameters;
- raw results;
- metrics;
- uncertainty;
- training logs;
- leakage prevention;
- reproducibility;
- source code.

Time budget:

**20+ minutes.**

## Audience D: MMC Reviewer

Question:

> Does this satisfy the capstone and demonstrate the curriculum?

They need:

- project plan;
- problem statement;
- impact statement;
- dataset;
- model workflow;
- fine-tuning;
- evaluation;
- responsible AI;
- reflection;
- clear curriculum mapping.

They receive a purpose-built `/capstone` pathway.

The MMC pathway must never dominate the project's main public identity.

---

# 8. Public Story

The main site should not open with:

> Domain Adaptation of Gemma 3 Through Parameter-Efficient Fine-Tuning...

That is technically correct and publicly terrible.

The public hero should be:

# ControlSift

## Can a small AI model tell **proof** from **paperwork**?

Supporting copy:

> Security teams collect mountains of evidence: policies, screenshots, access reports, logs, tickets and configuration exports.
>
> Some prove a control worked.
>
> Some only look convincing.
>
> ControlSift tests whether a small language model can learn the difference.

Technical supporting sentence:

> An applied AI research experiment comparing traditional machine learning, zero-shot and few-shot Gemma 3, and QLoRA-adapted Gemma 3 across approximately 1,500 synthetic cybersecurity evidence cases.

This creates progressive depth immediately.

---

# 9. Hero Evidence Example

Before showing charts, explain the problem with one example.

## CONTROL

Privileged administrative accounts must use multi-factor authentication.

## EVIDENCE A

> Company policy states that all privileged administrators are required to enroll in MFA.

### Expected assessment

**INSUFFICIENT**

Why:

The policy establishes an expectation but does not prove implementation.

## EVIDENCE B

> IAM export generated during the audit period lists all fourteen privileged administrative accounts and confirms MFA enrollment for each account.

### Expected assessment

**SUFFICIENT**

Why:

The evidence directly addresses the relevant control, population and period.

This example should appear almost immediately on the public site.

It explains the problem without requiring knowledge of:

- machine learning;
- GRC;
- LoRA;
- macro F1;
- transformers.

---

# 10. Public Headline Metrics

Once final results exist, the homepage should surface only three primary numbers.

Likely examples:

**1,500**  
Synthetic evidence cases

**5**  
Evidence-quality classes

**+XX.X**  
Macro-F1 improvement

The third number may change if another finding proves more meaningful.

Possibilities:

- challenge-set accuracy;
- reduction in a specific confusion pair;
- macro F1;
- percentage improvement over base Gemma.

Do not choose the metric based on which number looks largest.

Choose the metric that best communicates the real experimental result.

Before final results exist, display:

**Experiment in Progress**

Never put fictitious example metrics into production pages.

---

# 11. Core Classification Task

Each case contains:

1. control requirement;
2. environment;
3. evidence type;
4. evidence content;
5. expected evidence classification.

Model output:

```json
{
  "label": "CONTRADICTORY",
  "rationale": "The evidence shows a privileged account in scope without MFA enabled."
}
```

Primary evaluation is the classification label.

Rationale quality is secondary.

Do not use another proprietary LLM as the authoritative judge of rationale quality.

Human evaluation may be used for a sample.

---

# 12. Evidence Classes

## SUFFICIENT

Evidence adequately demonstrates the control for the relevant:

- scope;
- population;
- system;
- time period;
- control objective.

## PARTIAL

Evidence demonstrates meaningful operation but leaves material coverage unresolved.

Examples:

- 18 of 20 accounts represented;
- one of two production environments represented;
- incomplete audit period;
- sample does not cover required population.

## INSUFFICIENT

Evidence relates to the control but fails to demonstrate its operation.

Examples:

- policy requirement;
- procedure;
- administrator statement;
- undated screenshot;
- ticket describing intended configuration.

## IRRELEVANT

Evidence does not materially address the control.

Examples:

- antivirus report submitted for MFA;
- development evidence submitted for production scope;
- network diagram used to demonstrate account termination.

## CONTRADICTORY

Evidence affirmatively demonstrates that the requirement was not met.

Examples:

- privileged user without MFA;
- failed backup;
- terminated employee still active;
- encryption disabled;
- unauthorized change recorded in logs.

These definitions must be frozen before final test evaluation.

---

# 13. Dataset Scope

Target:

**Approximately 1,500 total examples**

Development benchmark:

```text
Train:       1,000
Validation:    200
Test:          200
```

Challenge set:

```text
Challenge:     100
```

Aim initially for balanced classes.

Five labels:

```text
200 training cases per class
40 validation cases per class
40 test cases per class
20 challenge cases per class
```

Balanced classes are appropriate because this is a controlled research benchmark rather than an attempt to reproduce real-world class prevalence.

---

# 14. Control Domains

Target broad coverage across at least ten domains:

1. Authentication
2. Identity and access management
3. Privileged access
4. Account lifecycle
5. Logging and monitoring
6. Change management
7. Vulnerability management
8. Patch management
9. Backup and recovery
10. Encryption
11. Endpoint security
12. Network security
13. Third-party controls

Avoid excessive dependence on IAM examples simply because IAM is easy to synthesize.

---

# 15. Evidence Artifact Types

Represent artifacts such as:

- configuration exports;
- IAM reports;
- access listings;
- screenshots;
- policy statements;
- procedures;
- change tickets;
- approval records;
- vulnerability scan reports;
- patch reports;
- backup-job results;
- restore tests;
- SIEM query output;
- log excerpts;
- firewall configurations;
- encryption configurations;
- endpoint-management reports;
- vendor attestations;
- administrative emails;
- exception records;
- self-attestations.

All artifacts remain synthetic.

---

# 16. Failure Taxonomy

Each case may contain one or more tags.

Recommended taxonomy:

```text
stale_evidence
wrong_period
scope_mismatch
population_gap
wrong_environment
wrong_system
missing_timestamp
policy_only
procedure_only
self_attestation
unverifiable_screenshot
sample_too_small
missing_approval
missing_execution_proof
source_conflict
contradictory_configuration
control_failure
incomplete_export
exception_unresolved
ownership_unclear
evidence_not_traceable
```

This taxonomy becomes useful for slice-based evaluation and the public Failure Lab.

---

# 17. Synthetic Data Generation

The benchmark should be reproducible without paid LLM APIs.

Create a deterministic synthetic-data generator.

Concept:

```text
Scenario Family
      |
      +--> Control requirement
      +--> Environment
      +--> Artifact
      +--> Valid evidence state
      |
      +--> Mutation Engine
             |
             +--> stale
             +--> incomplete population
             +--> wrong environment
             +--> policy only
             +--> missing date
             +--> contradictory state
             +--> irrelevant artifact
             +--> etc.
```

Use seeded pseudo-random generation.

Canonical seed:

```text
42
```

Generate:

- synthetic organizations;
- system names;
- account names;
- dates;
- ticket numbers;
- counts;
- percentages;
- environment names;
- report names.

Never use:

- employer data;
- CareCentrix evidence;
- customer information;
- real audit materials;
- real credentials;
- production logs;
- confidential control findings.

---

# 18. Dataset Schema

Recommended JSONL:

```json
{
  "id": "CS-IAM-0001",
  "scenario_family_id": "IAM-MFA-017",
  "variant_id": "A",
  "control_domain": "authentication",
  "control_statement": "Privileged accounts must use multi-factor authentication.",
  "environment": "production identity platform",
  "evidence_type": "IAM enrollment export",
  "evidence_text": "An export generated during the current audit period lists all privileged accounts and shows MFA enrollment for each account.",
  "label": "SUFFICIENT",
  "failure_tags": [],
  "difficulty": "easy",
  "generation_method": "synthetic_rule_based",
  "review_status": "unreviewed",
  "split": "train"
}
```

Optional analytical metadata:

```text
artifact_age_days
population_expected
population_observed
control_objective
source_system
notes
```

Hidden metadata must not leak into model input.

---

# 19. Leakage Prevention

This is mandatory.

Do not perform naive row-level random splitting after creating related variants.

Every generated scenario receives:

```text
scenario_family_id
variant_id
```

Example:

```text
IAM-MFA-017-A
IAM-MFA-017-B
IAM-MFA-017-C
```

All variants from one family belong to exactly one split.

Never place variants of the same underlying scenario across:

- training;
- validation;
- test;
- challenge.

CI should detect:

- exact duplicates;
- normalized duplicates;
- near duplicates;
- repeated scenario families across partitions;
- suspicious fuzzy similarity.

Leakage should fail CI.

---

# 20. Human Review Strategy

Do not falsely describe the dataset as fully human-labeled.

Primary labels are rule-derived within a controlled synthetic generation system.

Human review:

### Development corpus

Review a stratified sample across:

- every class;
- every major domain;
- difficulty levels;
- major failure tags.

Target roughly 10 percent.

### Challenge Set

Review **100 percent**.

Track:

```text
unreviewed
reviewed
corrected
```

Maintain:

`data/review_log.csv`

The Data Card must explain precisely how ground truth was produced.

---

# 21. Model Choice

Primary model:

`google/gemma-3-1b-it`

Reasons:

1. Direct relevance to the DeepMind curriculum.
2. Small enough for free GPU experimentation.
3. Appropriate for studying specialization.
4. Easier to reproduce than a larger model.
5. Avoids confusing model size with domain-adaptation quality.

The research question is not:

> How powerful a model can we afford?

It is:

> Can targeted adaptation materially improve a small model on a bounded domain task?

---

# 22. Technical Stack

Primary:

- Python
- PyTorch
- Hugging Face Transformers
- TRL
- PEFT
- bitsandbytes
- datasets
- accelerate
- scikit-learn
- pandas
- NumPy
- SciPy
- matplotlib

Optional:

- Jupyter
- TensorBoard
- Hugging Face Hub for adapter publication

Pin exact working versions after the first successful GPU smoke test.

Never rely on floating latest-version dependencies for final reproduction.

---

# 23. Zero-Cost Compute Architecture

Permanent source of truth:

**GitHub**

Temporary GPU:

1. Kaggle
2. Google Colab
3. Other genuinely free environment only if necessary

GitHub stores:

- source code;
- notebooks;
- dataset;
- documentation;
- configuration;
- predictions;
- metrics;
- figures;
- research report;
- public website.

GPU environments perform:

- model loading;
- quantized training;
- inference;
- adapter export.

They do not become the permanent home of the project.

Concept:

```text
GitHub
   |
   +--> source
   +--> dataset
   +--> notebooks
   +--> protocol
   |
   v
Kaggle / Colab GPU
   |
   +--> Gemma 3
   +--> QLoRA
   +--> training
   +--> evaluation
   |
   v
Generated artifacts
   |
   +--> predictions
   +--> logs
   +--> adapter metadata
   +--> metrics
   |
   v
GitHub
   |
   +--> CI
   +--> charts
   +--> research report
   +--> GitHub Pages
```

---

# 24. Benchmark Ladder

## Baseline 0

Majority class.

## Baseline 1

TF-IDF + logistic regression.

Input:

```text
control statement
+
evidence type
+
evidence text
```

This is more important than it may initially appear.

If a trivial lexical model performs extremely well, the synthetic benchmark may contain shortcuts.

That is a dataset-quality warning.

## Baseline 2

Gemma 3 zero-shot.

## Baseline 3

Gemma 3 few-shot.

Use one fixed representative example from each class.

## Model 4

Gemma 3 + QLoRA.

Final comparison:

```text
Majority
   |
TF-IDF
   |
Gemma Zero-Shot
   |
Gemma Few-Shot
   |
Gemma QLoRA
```

---

# 25. Evaluation Prompt

Use one canonical prompt after validation.

Example:

```text
You are evaluating cybersecurity control evidence.

Classify the evidence using exactly one label:

SUFFICIENT
PARTIAL
INSUFFICIENT
IRRELEVANT
CONTRADICTORY

CONTROL:
{control_statement}

ENVIRONMENT:
{environment}

EVIDENCE TYPE:
{evidence_type}

EVIDENCE:
{evidence_text}

Return valid JSON:

{
  "label": "<LABEL>",
  "rationale": "<one concise explanation>"
}
```

Prompt development uses validation examples.

Do not change the prompt based on held-out test failures.

---

# 26. Deterministic Inference

Where supported:

```text
temperature = 0
do_sample = false
```

Parser must handle:

- valid JSON;
- JSON-like output;
- extra prose;
- unknown labels;
- empty responses;
- malformed responses;
- refusals.

Ambiguous predictions must not be silently converted into correct labels.

Use:

`UNPARSEABLE`

when necessary.

---

# 27. QLoRA Configuration

Initial working configuration:

```text
quantization:           4-bit
quantization type:      NF4
double quantization:    enabled
LoRA rank:              16
LoRA alpha:             16
LoRA dropout:           0.05
epochs:                 3
learning rate:          2e-4 initial
max sequence length:    512
train batch:            1
eval batch:             1
seed:                   42
```

Gradient accumulation should be selected based on available VRAM.

LoRA target modules must be verified against the actual Gemma architecture.

Do not blindly copy module names from another transformer.

---

# 28. Training Monitoring

Capture:

- training loss;
- validation loss;
- learning rate;
- epoch;
- step;
- training duration;
- GPU model;
- GPU memory where practical;
- total parameter count;
- trainable parameter count;
- adapter size.

Checkpoint by epoch.

Evaluate checkpoints against validation data.

Model selection uses validation performance.

The held-out test set does not select models.

---

# 29. Test-Set Seal

The test set must be treated as a sealed research artifact.

Before final training:

1. generate test set;
2. validate;
3. manually review required portions;
4. freeze;
5. generate SHA-256 manifest;
6. commit;
7. tag research protocol.

Create an explicit repository tag such as:

```text
protocol-v1-locked
```

This commit should contain:

- research protocol;
- hypothesis definitions;
- dataset rules;
- evaluation rules;
- sealed test-set hash.

That creates a visible pre-results research contract.

---

# 30. Metrics

Primary:

**Macro F1**

Secondary:

- accuracy;
- macro precision;
- macro recall;
- weighted F1;
- per-class precision;
- per-class recall;
- per-class F1;
- confusion matrix;
- normalized confusion matrix;
- parse-success rate;
- challenge-set score.

Also record efficiency metrics:

- training time;
- adapter size;
- trainable parameter percentage;
- approximate GPU memory usage.

---

# 31. Statistical Comparison

Where appropriate:

- bootstrap confidence intervals;
- bootstrap interval for macro-F1 improvement;
- McNemar test on paired correct/incorrect predictions.

Report uncertainty.

Do not turn a tiny numerical improvement into a grand claim merely because it points upward.

---

# 32. Slice Analysis

Performance should be broken down by:

## Control domain

Examples:

- IAM
- logging
- change
- backup
- encryption

## Artifact type

Examples:

- policy
- screenshot
- export
- log
- ticket

## Difficulty

```text
easy
medium
hard
```

## Failure pathology

Examples:

- stale evidence;
- population gaps;
- policy-only evidence;
- scope mismatch;
- contradictory configuration.

This is where the project becomes especially useful for AI assurance.

---

# 33. Learning Curve

If compute permits, train with:

```text
100
250
500
1000
```

examples.

Hold other variables fixed.

Plot:

**Training examples versus Macro F1**

Public question:

> **How much specialized data did the model actually need?**

Potential findings may include:

- rapid early improvement;
- diminishing returns;
- continued scaling;
- no meaningful scaling.

All are legitimate outcomes.

---

# 34. Error Analysis

Create:

`reports/ERROR_ANALYSIS.md`

Classify failures into categories such as:

```text
scope reasoning
temporal reasoning
population reasoning
policy versus operation
contradiction detection
relevance judgment
label-boundary ambiguity
overgeneralization
```

Include cases where fine-tuning:

- corrected a baseline failure;
- failed to improve;
- introduced a regression.

Regressions should be highlighted, not hidden.

---

# 35. The Failure Lab

The public **Failure Lab** should become one of ControlSift's signature experiences.

Visitors select scenarios such as:

- Policy ≠ Proof
- Stale Evidence
- Wrong System
- Incomplete Population
- Contradictory Evidence
- Wrong Audit Period
- Looks Right, Isn't

Example:

## CONTROL

All terminated accounts must be disabled within 24 hours.

## EVIDENCE

HR termination record:

```text
Jane Doe
Termination: April 4
```

IAM export:

```text
Generated: April 9
Account: jdoe
Status: ACTIVE
```

Display:

### Base Gemma

`PARTIAL` ❌

### QLoRA Gemma

`CONTRADICTORY` ✅

### Expected

`CONTRADICTORY`

Explanation:

> The evidence does not merely fail to prove the control. It affirmatively shows that the control failed.

These should be precomputed results.

No live inference server is necessary.

---

# 36. Front-End Philosophy

Do not build:

- generic Streamlit dashboard;
- glowing AI robot;
- cyberpunk circuit board;
- animated brain;
- gimmicky AI chat window.

Visual language should come from:

- documents;
- evidence snippets;
- classification states;
- experiment results;
- typography;
- restrained charts;
- technical metadata.

Desired feel:

> **small independent research laboratory**

Not:

> student AI demo.

Dark-mode is appropriate, but restrained.

Use:

- spacious typography;
- clean cards;
- high contrast;
- subtle technical metadata;
- evidence-document motifs;
- thin charts;
- limited visual clutter.

---

# 37. Public Site Structure

Primary navigation:

```text
Home
Failure Lab
Results
Methods
Responsible AI
Reproduce
```

MMC capstone view:

```text
/capstone/
```

This does not need prominent primary-navigation placement.

Footer link is enough.

---

# 38. Home Page

Structure:

## Hero

ControlSift

**Can a small AI model tell proof from paperwork?**

## Problem

Simple evidence example.

## Three Numbers

Headline results.

## Before / After

Base versus tuned model.

## What We Tested

Short pipeline:

```text
Synthetic Evidence
      |
Base Gemma
      |
QLoRA
      |
Held-Out Evaluation
```

## What Improved

Headline finding.

## What Still Fails

Headline limitation.

## Explore

Buttons:

```text
Enter Failure Lab
See the Numbers
Read the Research
View GitHub
```

---

# 39. Results Page

This is the numbers crowd's entrance.

Show:

## Model Comparison

```text
Majority
TF-IDF
Gemma zero-shot
Gemma few-shot
Gemma QLoRA
```

Metrics:

- macro F1;
- accuracy;
- precision;
- recall;
- challenge performance.

## Per-Class Performance

All five classes.

## Confusion Matrix

Raw and normalized.

## Learning Curve

If available.

## Slice Analysis

Performance by:

- domain;
- evidence artifact;
- difficulty;
- failure type.

## Statistical Comparison

Confidence intervals and paired testing.

## Compute Profile

Show:

- model size;
- trainable parameter count;
- adapter size;
- training duration;
- runtime GPU.

---

# 40. "Receipts" Layer

Every polished conclusion should be traceable to underlying evidence.

Make available:

- research protocol;
- dataset card;
- model card;
- dataset manifest;
- hashes;
- configurations;
- raw predictions;
- machine-readable metrics;
- statistical output;
- error analysis;
- training logs;
- notebooks;
- source.

The project should itself demonstrate evidence provenance.

That is thematically appropriate.

---

# 41. Responsible AI Page

Prominently state:

> **ControlSift is a research benchmark, not an automated audit or compliance decision system.**

Discuss:

- automation bias;
- false assurance;
- synthetic-to-real gap;
- classification errors;
- domain drift;
- model-version drift;
- incomplete contextual understanding;
- rationale hallucination;
- overconfidence;
- human oversight.

Also explain:

> A model that becomes better at categorizing synthetic evidence has not thereby become qualified to perform autonomous control testing.

---

# 42. Synthetic-to-Real Gap

This should be treated as a major limitation.

Strong performance on synthetic cases does not prove equivalent performance on:

- production evidence;
- screenshots;
- scanned records;
- multiple conflicting documents;
- organization-specific jargon;
- incomplete audit packages;
- legacy exports;
- unusual system architectures;
- messy human-generated tickets;
- ambiguous controls.

State this prominently.

It strengthens the research.

It does not weaken it.

---

# 43. Dataset Card

Create:

`governance/DATA_CARD.md`

Include:

- purpose;
- composition;
- synthetic origin;
- labeling methodology;
- review methodology;
- class balance;
- control domains;
- scenario-family design;
- split methodology;
- leakage prevention;
- known limitations;
- appropriate use;
- inappropriate use.

---

# 44. Model Card

Create:

`governance/MODEL_CARD.md`

Include:

- base model;
- model version;
- fine-tuning method;
- adapter configuration;
- training environment;
- dataset version;
- intended use;
- test results;
- challenge results;
- failure modes;
- limitations;
- human oversight expectations.

---

# 45. AI Risk Register

Create:

`governance/AI_RISK_REGISTER.md`

Suggested risks:

```text
automation bias
false assurance
misclassification
scope misunderstanding
synthetic-to-real gap
hallucinated rationale
benchmark overfitting
model drift
dataset artifact learning
domain shift
```

For each:

```text
Risk
Cause
Impact
Likelihood
Severity
Mitigation
Residual risk
```

---

# 46. Repository Architecture

```text
controlsift/
|
|-- README.md
|-- LICENSE
|-- CITATION.cff
|-- CONTRIBUTING.md
|-- SECURITY.md
|-- AGENTS.md
|-- pyproject.toml
|-- requirements.txt
|-- requirements-dev.txt
|-- .gitignore
|
|-- configs/
|   |-- baseline.yaml
|   |-- gemma3_1b_qlora.yaml
|   `-- evaluation.yaml
|
|-- data/
|   |-- README.md
|   |
|   |-- manifests/
|   |   `-- dataset_manifest.json
|   |
|   |-- scenarios/
|   |   `-- scenario_families.yaml
|   |
|   |-- processed/
|   |   |-- train.jsonl
|   |   |-- validation.jsonl
|   |   |-- test.jsonl
|   |   `-- challenge.jsonl
|   |
|   `-- review_log.csv
|
|-- notebooks/
|   |-- 01_dataset_exploration.ipynb
|   |-- 02_traditional_baseline.ipynb
|   |-- 03_gemma_baseline.ipynb
|   |-- 04_gemma_qlora_training.ipynb
|   |-- 05_final_evaluation.ipynb
|   `-- 06_error_analysis.ipynb
|
|-- src/
|   `-- controlsift/
|       |
|       |-- data/
|       |   |-- generate.py
|       |   |-- validate.py
|       |   |-- split.py
|       |   `-- schema.py
|       |
|       |-- prompting/
|       |   `-- templates.py
|       |
|       |-- training/
|       |   |-- train.py
|       |   `-- config.py
|       |
|       |-- evaluation/
|       |   |-- evaluate.py
|       |   |-- parser.py
|       |   |-- metrics.py
|       |   |-- slices.py
|       |   `-- statistics.py
|       |
|       `-- visualization/
|           `-- charts.py
|
|-- scripts/
|   |-- generate_dataset.py
|   |-- validate_dataset.py
|   |-- run_tfidf_baseline.py
|   |-- run_gemma_baseline.py
|   |-- run_evaluation.py
|   `-- build_figures.py
|
|-- results/
|   |-- README.md
|   |-- majority/
|   |-- tfidf/
|   |-- gemma_zero_shot/
|   |-- gemma_few_shot/
|   |-- gemma_qlora/
|   |-- predictions/
|   |-- metrics/
|   `-- manifests/
|
|-- reports/
|   |-- RESEARCH_REPORT.md
|   |-- ERROR_ANALYSIS.md
|   `-- figures/
|
|-- governance/
|   |-- DATA_CARD.md
|   |-- MODEL_CARD.md
|   |-- AI_RISK_REGISTER.md
|   |-- INTENDED_USE.md
|   |-- LIMITATIONS.md
|   `-- HUMAN_REVIEW.md
|
|-- tests/
|   |-- test_schema.py
|   |-- test_dataset_integrity.py
|   |-- test_split_leakage.py
|   |-- test_output_parser.py
|   |-- test_metrics.py
|   `-- test_reproducibility.py
|
|-- docs/
|   |-- index.html
|   |-- failure-lab.html
|   |-- results.html
|   |-- methods.html
|   |-- responsible-ai.html
|   |-- reproduce.html
|   |
|   |-- capstone/
|   |   `-- index.html
|   |
|   |-- assets/
|   |   |-- css/
|   |   |-- js/
|   |   `-- img/
|   |
|   `-- data/
|       |-- results.json
|       `-- failure_lab.json
|
`-- .github/
    |-- workflows/
    |   |-- ci.yml
    |   `-- pages.yml
    |
    `-- dependabot.yml
```

---

# 47. GitHub Actions

On pull request and push:

1. install environment;
2. run formatting/linting;
3. run tests;
4. validate schema;
5. check split integrity;
6. check class distribution;
7. detect duplicates;
8. detect scenario-family leakage;
9. validate machine-readable results;
10. regenerate static figures where appropriate;
11. verify public metrics correspond to stored results.

Do not:

- download Gemma;
- perform GPU training;
- run full model inference.

CI validates research artifacts.

It does not become the compute environment.

---

# 48. Results Integrity

Every result displayed publicly must originate in machine-readable output.

Example:

```json
{
  "experiment": "gemma3_1b_qlora",
  "dataset_version": "1.0.0",
  "model": "google/gemma-3-1b-it",
  "seed": 42,
  "metrics": {
    "accuracy": null,
    "macro_f1": null,
    "macro_precision": null,
    "macro_recall": null
  }
}
```

Before execution:

`null`

Never fabricate realistic-looking placeholder results.

---

# 49. Visualization Pipeline

Generate charts from result files.

Required figures:

1. model comparison;
2. per-class F1;
3. confusion matrix;
4. normalized confusion matrix;
5. learning curve;
6. performance by failure type;
7. performance by domain;
8. training and validation loss;
9. baseline versus tuned outcomes;
10. challenge-set comparison.

Build with:

```text
python scripts/build_figures.py
```

Website graphics must never contain manually invented values.

---

# 50. MMC Capstone Layer

Create a dedicated:

`/capstone/`

Title:

# Applied AI Research Capstone

This page exists to make MMC evaluation easy.

It should include:

## Problem Statement

Cybersecurity teams must distinguish artifacts that substantively demonstrate control operation from evidence that is incomplete, irrelevant, stale, or contradictory.

## Research Aim

Investigate whether domain adaptation using QLoRA improves a small language model's performance on this bounded task.

## Intended Impact

Explore whether small, specialized language models could eventually assist human reviewers in evidence triage while explicitly studying the risks of false assurance and inappropriate automation.

## Dataset

Explain:

- synthetic generation;
- labeling;
- review;
- boundaries;
- consent/privacy advantages;
- limitations.

## Model Development

Explain:

- Gemma 3;
- transformers;
- tokenized language representation;
- QLoRA;
- GPU training;
- training monitoring.

## Evaluation

Explain:

- baselines;
- held-out test;
- challenge set;
- macro F1;
- error analysis.

## Responsible Innovation

Explain:

- human oversight;
- automation bias;
- Data Card;
- Model Card;
- risk register;
- limitations.

## Reflection

Discuss:

- what changed;
- what did not;
- unexpected results;
- what the benchmark failed to represent;
- what should be studied next.

Buttons:

```text
Explore Research Site
View GitHub
Read Research Report
Read Data Card
Read Model Card
```

---

# 51. DeepMind Curriculum Mapping

The MMC capstone pathway should explicitly map coursework to implementation.

Suggested mapping:

| Learning area | ControlSift implementation |
|---|---|
| Language-model foundations | Model selection, task framing, baseline reasoning |
| Train a small language model | Training concepts, loss monitoring and model-development workflow |
| Represent language data | Dataset structure, tokenizer-compatible formatting and preprocessing |
| Design and train neural networks | Training dynamics, overfitting, validation and generalization |
| Transformer architecture | Gemma 3 transformer |
| Fine-tune your model | QLoRA domain adaptation |
| Accelerate your model | Quantization and GPU training |
| Responsible capstone development | Data Card, Model Card, AI risk analysis, evaluation and research report |

The point is to make the curriculum visible through actual work.

---

# 52. MMC Branding Rule

The main README must **not** open with:

> This is my Mentor Me Collective capstone.

MMC acknowledgement belongs near the bottom.

Suggested wording:

> ControlSift was developed as an independent applied-AI research project following participation in Google DeepMind's AI Research Foundations curriculum through Mentor Me Collective.

No sarcasm in public project materials.

The quality difference should make the point without commentary.

---

# 53. Optional SDG / Community Alignment

Do not invent Sustainable Development Goal alignment unless MMC requires it.

If the final rubric requires explicit SDG mapping, evaluate the actual requirement first.

Potential honest connections may include:

- stronger institutional accountability;
- accessible technical capability for resource-constrained organizations;
- trustworthy adoption of AI systems.

Do not staple an unrelated UN goal onto the project merely for decoration.

If MMC requires a specific format, create the mapping in the capstone layer without redefining ControlSift's public purpose.

---

# 54. Research Report

Create:

`reports/RESEARCH_REPORT.md`

Target sections:

1. Abstract
2. Introduction
3. Research Question
4. Hypotheses
5. Background
6. Dataset
7. Label Ontology
8. Experimental Design
9. Baselines
10. QLoRA Adaptation
11. Results
12. Statistical Analysis
13. Error Analysis
14. Challenge Set
15. Responsible AI
16. Limitations
17. Future Research
18. Conclusion

Write the conclusion after results exist.

Do not write the answer before running the experiment.

---

# 55. GitHub README

README order:

```text
ControlSift

Can a small AI model tell proof from paperwork?

hero visual

Why this matters

one evidence example

headline findings

research question

benchmark

model ladder

key results

what the model still gets wrong

Failure Lab link

methodology

reproduction

responsible use

research report

repository structure

acknowledgements
```

The README should work for someone unwilling to click the research site.

---

# 56. Portfolio Integration

After v1.0, add a project card to the primary portfolio.

Suggested:

## ControlSift

**Can a small AI model tell proof from paperwork?**

> Domain-adapted Gemma 3 using QLoRA to evaluate cybersecurity control evidence across a purpose-built synthetic benchmark.

Tags:

```text
Gemma 3
QLoRA
Applied ML
AI Assurance
Model Evaluation
GRC
```

Once final results exist:

```text
1,500
Evidence Cases

5
Evidence Classes

+XX.X
Macro-F1 Improvement
```

Links:

```text
Explore Research
GitHub
```

Do not prominently label the portfolio card:

`MMC Capstone`

---

# 57. Resume Extraction

Do not add fabricated results.

Pre-results version:

> Designed an applied ML research benchmark for cybersecurity control-evidence assessment, comparing classical ML, zero-/few-shot Gemma 3 and QLoRA-based domain adaptation across approximately 1,500 synthetic evidence scenarios.

Post-results version:

> Fine-tuned Gemma 3 using QLoRA for cybersecurity control-evidence classification, improving held-out macro F1 from **[BASE]** to **[TUNED]** across five evidence-quality classes while documenting domain-specific failure modes and responsible-use limitations.

AI governance variant:

> Designed an end-to-end AI assurance experiment combining synthetic dataset governance, Gemma 3 QLoRA fine-tuning, held-out evaluation, error analysis, Data/Model Cards and an AI risk register.

---

# 58. Interview Narrative

The project should support this explanation:

> I wanted to test whether a small general-purpose language model could actually learn a narrow GRC judgment task rather than simply sound convincing when discussing it. I created a synthetic benchmark of control-evidence scenarios, established traditional ML and zero-/few-shot Gemma baselines, fine-tuned Gemma 3 using QLoRA, and evaluated the adapted model using a held-out benchmark and separate challenge set. The important part wasn't just whether the metrics improved. I analyzed which evidence defects remained difficult and documented where the model should not be trusted.

That is the career payoff.

---

# 59. Project Management Structure

Use GitHub Issues or Work/Codex task tracking with these epics:

```text
EPIC-01 Foundation
EPIC-02 Research Protocol
EPIC-03 Dataset Engine
EPIC-04 Dataset Quality
EPIC-05 Classical Baseline
EPIC-06 Gemma Baselines
EPIC-07 QLoRA Training
EPIC-08 Final Evaluation
EPIC-09 Error Analysis
EPIC-10 Responsible AI
EPIC-11 Research Site
EPIC-12 MMC Capstone
EPIC-13 Research Report
EPIC-14 Public Release
EPIC-15 Portfolio / Resume
```

Suggested labels:

```text
research
data
ml
evaluation
frontend
governance
documentation
capstone
bug
integrity
release
optional
```

---

# 60. Codex Operating Rules

Create `AGENTS.md`.

Non-negotiable instructions:

## Research Integrity

- Never fabricate results.
- Never manufacture placeholder metrics.
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

- Use fixed seeds where practical.
- Store configuration separately.
- log dependency versions;
- log hardware;
- log dataset hashes;
- log model ID;
- preserve predictions.

## Website

- No fabricated statistics.
- No glowing AI robot imagery.
- Progressive disclosure.
- Main site optimized for public comprehension.
- Technical evidence remains accessible.

## Scope Discipline

Do not expand v1 into:

- SaaS;
- live inference;
- RAG;
- agent workflows;
- document ingestion;
- OCR;
- authentication;
- production GRC software.

---

# 61. Four-Month Working Runway

Official MMC dates may change.

This is an internal execution cadence beginning before formal kickoff.

## Month 1: Foundation and Dataset

Goals:

- repository scaffold;
- project branding;
- protocol;
- schema;
- labeling rules;
- scenario families;
- synthetic generator;
- dataset validation;
- initial public-site shell.

Deliverable:

**We have a legitimate benchmark before touching Gemma.**

## Month 2: Baselines and Training

Goals:

- TF-IDF baseline;
- Gemma environment;
- zero-shot;
- few-shot;
- QLoRA smoke test;
- full fine-tuning;
- validation monitoring.

Deliverable:

**We have comparative model behavior.**

## Month 3: Research Results

Goals:

- final held-out test;
- challenge set;
- statistical analysis;
- slice analysis;
- learning curve;
- error analysis;
- Data Card;
- Model Card;
- risk register.

Deliverable:

**We know what happened and why it matters.**

## Month 4: Sizzle and Release

Goals:

- Failure Lab;
- polished public site;
- research report;
- MMC capstone page;
- README;
- v1.0 release;
- portfolio card;
- resume bullets;
- launch material.

Deliverable:

**Research becomes a career artifact.**

Because development begins before official kickoff, there is no requirement to consume all four months.

A strong project completed early is preferable to artificial delay.

---

# 62. Phase Gates

Do not simply march forward because a task is complete.

Use quality gates.

## Gate 1: Dataset Validity

Before Gemma:

- schema valid;
- classes balanced;
- scenario families isolated;
- no obvious lexical leakage;
- TF-IDF behavior understood.

## Gate 2: Protocol Lock

Before final training:

- hypotheses frozen;
- metric frozen;
- test set sealed;
- prompt strategy frozen;
- evaluation procedure documented.

## Gate 3: Model Validity

Before final testing:

- adapter reloads;
- training stable;
- validation works;
- outputs parse correctly.

## Gate 4: Research Validity

Before public claims:

- final test complete;
- challenge set complete;
- statistics complete;
- error analysis complete;
- limitations documented.

## Gate 5: Public Release

Before v1.0:

- README polished;
- Pages polished;
- links tested;
- results traceable;
- no secrets;
- governance docs complete.

---

# 63. Project Risks

## Risk: Free GPU unavailable

Mitigation:

- Kaggle primary;
- Colab fallback;
- keep model at 1B;
- reduce experimental runs before paying.

## Risk: Gemma access issues

Mitigation:

- verify model access early;
- complete smoke test before depending on final schedule.

## Risk: Dataset too templated

Mitigation:

- TF-IDF baseline;
- lexical analysis;
- varied scenario families;
- challenge set;
- human review.

## Risk: Fine-tuning overfits

Mitigation:

- validation monitoring;
- fewer epochs;
- LoRA capacity adjustment;
- frozen test set.

## Risk: Benchmark becomes too easy

Mitigation:

- harder challenge set;
- nested deficiencies;
- ambiguous boundaries;
- remove obvious label keywords.

## Risk: Scope explosion

Mitigation:

- no backend;
- no RAG;
- no document upload;
- no live inference;
- v1 research first.

## Risk: Project name collision

Mitigation:

- perform final GitHub/web/trademark sanity search immediately before public branding.

## Risk: MMC requirement changes

Mitigation:

- capstone layer remains modular;
- research project does not depend on MMC rubric.

---

# 64. What We Deliberately Do Not Build in v1

No:

- enterprise login;
- cloud backend;
- database;
- live chatbot;
- document ingestion;
- PDF processing;
- OCR;
- vector store;
- RAG;
- agent framework;
- production audit workflow;
- billing;
- hosted inference endpoint;
- compliance dashboard.

These features make the project larger without making the research better.

---

# 65. Optional Future Extensions

Only after v1.0.

## Legacy Control Lab Bridge

Use synthetic legacy-system evidence as an out-of-domain benchmark.

Question:

> Can a model trained on conventional control evidence recognize equivalent control evidence from legacy platforms?

This could become particularly interesting for IBM i evidence.

## AI Assurance Range Integration

Use ControlSift as an evaluation workload for:

- model swaps;
- prompt regressions;
- corrupted evidence;
- adversarial framing;
- benchmark regression.

## Multi-Artifact Evidence Packages

Move from one evidence artifact to several related artifacts.

## Human-versus-Model Study

Compare model classifications against independent practitioners.

## Model Comparisons

Test additional small open models.

None of these should block v1.0.

---

# 66. Launch Experience

A visitor should be able to enter at different depths.

## 60 Seconds

Understand:

> AI must distinguish evidence that proves something from paperwork that merely mentions it.

## Five Minutes

Explore Failure Lab and before/after model behavior.

## Twenty Minutes

Inspect:

- benchmarks;
- confusion matrices;
- learning curve;
- failure slices.

## Deep Dive

Clone:

- dataset;
- scripts;
- notebooks;
- configurations;
- raw predictions.

This progressive-depth strategy is mandatory.

---

# 67. Launch Assets

Prepare:

## GitHub

- README
- release
- research report
- screenshots
- citation file

## Portfolio

- project card
- hero image
- metrics
- research link

## LinkedIn

Optional launch post emphasizing the question and result rather than the course.

## Resume

One technical bullet and one governance-oriented variant.

## Interviews

30-second, 90-second and deep-dive explanations.

## MMC

Dedicated submission bundle.

One project produces every asset.

---

# 68. MMC Submission Bundle

Prepare:

```text
Project title
Executive summary
Problem statement
Impact statement
Research question
Dataset description
Model development methodology
Fine-tuning approach
Evaluation methodology
Responsible AI discussion
Reflection
GitHub repository
Research site
Research report
Data Card
Model Card
Final visual summary
```

If MMC wants slides, generate slides from these existing artifacts.

Do not perform separate technical work solely to create an MMC version.

---

# 69. Suggested v1 Release History

```text
v0.1.0  repository foundation
v0.2.0  dataset generator
v0.3.0  benchmark v1
v0.4.0  classical baseline
v0.5.0  Gemma baselines
v0.6.0  QLoRA training
v0.7.0  final evaluation
v0.8.0  error and governance analysis
v0.9.0  public research experience
v1.0.0  complete release
```

Create a separate protocol-lock tag before final results.

---

# 70. Definition of Done

ControlSift v1.0 is finished when:

## Research

- question documented;
- hypotheses documented;
- research protocol locked;
- results measured;
- uncertainty considered;
- conclusions supported.

## Dataset

- approximately 1,500 cases;
- five classes;
- multiple domains;
- deterministic generation;
- Data Card;
- no scenario-family leakage;
- human review documented.

## Modeling

- majority baseline;
- TF-IDF baseline;
- Gemma zero-shot;
- Gemma few-shot;
- Gemma QLoRA.

## Evaluation

- held-out test;
- challenge set;
- macro F1;
- class-level metrics;
- confusion matrices;
- slice analysis;
- error analysis;
- raw predictions available.

## Responsible AI

- Model Card;
- Data Card;
- risk register;
- intended use;
- prohibited use;
- human-review expectations;
- synthetic-data limitation.

## Engineering

- clean repository;
- CI passing;
- test suite;
- result integrity;
- reproducible configuration;
- secrets absent.

## Public Experience

- GitHub Pages live;
- strong hero;
- Failure Lab;
- numbers layer;
- methods;
- responsible AI;
- reproducibility.

## MMC

- capstone page;
- curriculum mapping;
- reflection;
- submission bundle.

## Career

- portfolio card;
- resume bullet;
- interview narrative;
- public research artifact.

---

# 71. Final Quality Standard

The finished project should survive four different reactions.

### Recruiter

> I understand what this does, and this is much more substantial than another AI demo.

### GRC Practitioner

> These are recognizable evidence problems, and the project isn't pretending the AI replaces judgment.

### ML Reviewer

> The experimental design is reproducible, the benchmark isn't obviously leaking, and the author actually evaluated generalization and failure.

### MMC Reviewer

> Every major learning objective is visibly demonstrated in the capstone.

If all four reactions are defensible, the project succeeded.

---

# 72. Final Public Position

ControlSift should never depend on the viewer caring about MMC, Google Skills, or a course badge.

The final public artifact says:

> **Here is a research question.**
>
> **Here is the benchmark I created.**
>
> **Here is the base model.**
>
> **Here is how I adapted it.**
>
> **Here is how I tested it.**
>
> **Here is what improved.**
>
> **Here is what failed.**
>
> **Here are the receipts.**
>
> **Here is where you should not trust it.**

That is the project.

The course is merely how we got invited to dinner.