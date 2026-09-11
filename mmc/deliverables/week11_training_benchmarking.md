# Week 11 deliverable - Training & Benchmarking

**Handbook:** Course 08 · Capstone – Training & Benchmarking  
**Key deliverable:** Final trained-model artifacts, tracking receipts & comparative analysis

## 1. Completed experiments

| ID | Experiment | Dataset | Output dir | Test macro F1 |
|----|------------|---------|------------|---------------|
| B2 | Gemma 3 1B zero-shot | v1.0.0 | `results/gemma_zero_shot/` | ~0.080 |
| B3 | Gemma 3 1B few-shot | v1.0.0 | `results/gemma_few_shot/` | ~0.137 |
| M4 | Gemma 3 1B QLoRA | v1.0.0 | `results/gemma_qlora/` | ~0.083 |

QLoRA configuration: `configs/gemma3_1b_qlora.yaml` - r=16, alpha=16, 4-bit NF4, bf16 compute, grad accumulation 8, seed 42.

Within the controlled Gemma v1.0 ladder, **few-shot prompting is strongest**. QLoRA doesn't beat few-shot and QLoRA test parse success is about **0.435**, making output-contract reliability a material part of the result.

## 2. Comparative analysis artifact

Machine-readable table:

```bash
python -m mmc.labs.week11_comparative
```

Output: `mmc/deliverables/outputs/week11_comparative_analysis.json`  
Public result ledger: `docs/data/results.json`

The comparative artifact carries the final dataset-version boundary: classical experiments use v1.1.0 while Gemma experiments use v1.0.0. Cross-version values are descriptive only, not a controlled same-benchmark ranking.

## 3. Failure analysis

- Failure Lab: `docs/failure-lab.html` / `docs/data/failure_lab.json`
- Error analysis: `reports/ERROR_ANALYSIS.md`
- Gemma result receipts: `results/gemma_zero_shot/`, `results/gemma_few_shot/`, `results/gemma_qlora/`

The final analysis preserves both classification errors and output-parse failures rather than repairing model output silently.

## 4. Artifacts and receipts

| Artifact | Path | Status |
|----------|------|--------|
| Toy LoRA scaffold (Week 7) | `mmc/deliverables/outputs/week07_lora_adapter.npz` | complete |
| QLoRA experiment receipts | `results/gemma_qlora/` | complete |
| Gemma zero-shot receipts | `results/gemma_zero_shot/` | complete |
| Gemma few-shot receipts | `results/gemma_few_shot/` | complete |
| Comparative JSON | `mmc/deliverables/outputs/week11_comparative_analysis.json` | complete |
| Failure analysis | `reports/ERROR_ANALYSIS.md` | complete |

## 5. Status

`meets` - training, evaluation, comparative analysis, failure analysis, and result receipts are complete. The final record explicitly preserves the v1.1 classical / v1.0 Gemma version boundary.
