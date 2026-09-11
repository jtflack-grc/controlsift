# Week 8 deliverable - Model Alignment & Safety Report

**Handbook focus:** RLHF / DPO overview, alignment, safety, red-teaming mindset.  
**ControlSift scope note:** v1 does **not** train a reward model or run DPO. This report documents alignment *practice* used by the project and explicit non-claims.

## 1. Alignment goal for ControlSift

Desired behavior: emit one of five evidence-quality labels consistently with sealed ground truth for research measurement; never present scores as audit decisions.

## 2. Starting point

- Base model: Gemma 3 1B **Instruct** (instruction-tuned priors).
- Task adaptation path: supervised QLoRA (planned) - SFT, not preference optimization.

## 3. Behavioral constraints

| Control | Mechanism |
|---------|-----------|
| Constrained label space | Prompt + parser |
| Invalid outputs | Counted as errors (no silent remapping) |
| Decoding | temperature 0.0 / greedy for scored runs |
| Intended use | Research / education / method comparison only |
| Bright lines | No production auditor; no secrets; no fabricated metrics |

## 4. Safety / misuse analysis (lightweight red-team)

| Scenario | Risk | Mitigation |
|----------|------|------------|
| User treats model as auditor | False assurance | Intended Use + risk register; human judgment authoritative |
| Schema gaming on synthetic packets | Overstated generalization | RESEARCH_SURFACE disclosure; Failure Lab |
| Prompt injection to force SUFFICIENT | Harmful rubber-stamp | Parser + evaluation protocol; refuse productization |
| Training on private evidence | Privacy breach | Synthetic-only corpus policy |
| Preference hacking via RLHF (not used) | N/A in v1 | Explicit non-use of RLHF/DPO |

## 5. Toxicity / safety evaluations

Not applicable as a chat product. Evaluation is classification accuracy / macro F1 on sealed splits. No open-ended generation deployment.

## 6. Relation to RLHF / DPO coursework

| Concept | Course expectation | ControlSift response |
|---------|--------------------|----------------------|
| RLHF | Overview / optional labs | Understood; **not implemented** in v1 |
| DPO | Preference pairs | **Not implemented** |
| Reward model | Safety scoring | Replaced by rule-derived labels + governance |
| Red-teaming | Adversarial prompts | Documented misuse scenarios above |

## 7. Artifacts

- `governance/INTENDED_USE.md`
- `governance/AI_RISK_REGISTER.md`
- `governance/MODEL_CARD.md`
- `governance/LIMITATIONS.md`
- `docs/assurance/` HTML mirrors

## 8. Conclusion

Alignment for this project is **use-alignment + evaluation honesty**, not preference-model training. That matches a research classifier and avoids overclaiming RLHF completion.
