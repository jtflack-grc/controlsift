# Model Card - ControlSift Gemma 3 QLoRA Adapter

## Model details

| Item | Value |
|------|-------|
| Base model | `google/gemma-3-1b-it` |
| Adaptation | QLoRA (4-bit NF4, double quant, LoRA r=16, α=16, dropout 0.05) |
| Task | 5-class control-evidence quality classification |
| Framework | PyTorch, Transformers, PEFT, TRL, bitsandbytes |
| Training entrypoint | `python -m controlsift.training.train` |

LoRA target modules are **resolved from the loaded architecture** via `resolve_lora_target_modules` - not copied blindly from unrelated models.

## Intended use

Research comparison of prompting vs PEFT on a synthetic evidence benchmark; educational / portfolio demonstration of evaluation rigor.

## Out-of-scope / prohibited use

- Automated audit or compliance certification
- Regulatory decision-making
- Replacement for control owners or auditors
- Scoring real customer evidence in production without human review
- Claims of real-world compliance determination

## Training data

ControlSift synthetic train split (seed 42). See Data Card.

## Evaluation data

Sealed validation / test / challenge JSONL. Metrics in `results/gemma_qlora/` after GPU runs.

## Metrics

Primary: **macro F1**. Also accuracy, macro precision/recall, per-class scores, confusion matrices, parse-success rate, challenge-set score.

## Ethical considerations

Synthetic data only. Risk of over-trust if public metrics are misread as production readiness. See `AI_RISK_REGISTER.md`.

## Caveats

Until GPU experiments complete, public macro F1 for Gemma variants remains `null`. Don't invent placeholder scores.
