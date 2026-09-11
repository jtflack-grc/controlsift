# Portfolio Card - ControlSift

**ControlSift**  
*Can a small AI model tell proof from paperwork?*

Applied AI assurance research project: a leakage-controlled synthetic benchmark for five-class cybersecurity evidence quality, classical baselines, Gemma 3 zero-shot and few-shot prompting, QLoRA adaptation, failure analysis, and explicit research-governance controls.

**Published result boundary**

- Classical experiments: dataset **v1.1.0**; Majority macro F1 **0.067**; TF-IDF **~0.53** test / **~0.52** challenge
- Gemma experiments: dataset **v1.0.0**; zero-shot **~0.080**, few-shot **~0.137**, QLoRA **~0.083** test macro F1
- Within Gemma v1.0, few-shot was strongest; QLoRA didn't beat few-shot and test parse success was about **0.435**
- Classical v1.1 and Gemma v1.0 scores are descriptive across versions, not a controlled same-benchmark ranking
- Research surface: compositional synthetic evidence packets, not raw customer binders

**Highlights**

- Built a ~1,500-case synthetic evidence benchmark with scenario-family split'solation and integrity CI
- Detected TF-IDF saturation (1.0), hardened the generator, and re-baselined the classical benchmark to a materially harder ~0.53 macro F1
- Preserved an inconvenient negative model result rather than manufacturing an AI win
- Published machine-readable results, a Failure Lab, Data Card, Model Card, risk register, human-review boundaries, and reproducibility guidance
- Documented the dataset-version mismatch explicitly rather than presenting a false cross-family leaderboard

**Status:** Complete research artifact and MMC / Google DeepMind AI Research Foundations capstone.

**Links:** GitHub · GitHub Pages · Research report · Assurance · Final presentation
