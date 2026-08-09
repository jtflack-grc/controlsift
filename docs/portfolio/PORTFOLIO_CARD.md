# Portfolio Card — ControlSift

**ControlSift**  
*Can a small AI model tell proof from paperwork?*

Applied AI research project: leakage-controlled synthetic benchmark for five-class cybersecurity evidence quality, classical baselines under a sealed protocol, and a public Failure Lab. Gemma 3 prompting + QLoRA are **instrumented and ready**; metrics stay `null` until gated GPU runs land.

**Status (honest)**

- Dataset **v1.1.0**, protocol tag `protocol-v1-locked`
- Majority macro F1 **0.067** · TF-IDF **~0.53** test / **~0.52** challenge
- Gemma zero-shot / few-shot / QLoRA: **not run yet**
- Research surface: compositional evidence packets (disclosed) — not raw customer binders

**Highlights**

- Built a ~1,500-case synthetic evidence benchmark with scenario-family split isolation and integrity CI
- Detected TF-IDF saturation (1.0), hardened the generator, and re-baselined to an uncomfortable lexical ceiling
- Locked evaluation (hashes + frozen prompt) before LLM claims; public site refuses fabricated metrics
- Documented Data Card, Model Card, risk register, and label-audit limits (structural + scripted spot-check — not full human gold)

**Next**

HF license + Kaggle GPU → `notebooks/kaggle_runner.ipynb` → commit `results/gemma_*`

**Links:** GitHub · GitHub Pages · Research report · Assurance
