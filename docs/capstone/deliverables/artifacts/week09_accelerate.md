# Week 9 deliverable — Accelerated fine-tuning pipeline notes

**Handbook milestone:** Optimized fine-tuning pipeline with memory profiling logs (FP16/BF16, INT4/INT8, gradient accumulation).

## Pipeline configuration (ControlSift / Gemma 3 1B QLoRA)

Source of truth: `configs/gemma3_1b_qlora.yaml`

| Technique | Setting |
|-----------|---------|
| Quantization | 4-bit NF4, double quant |
| Compute dtype | bfloat16 |
| LoRA | r=16, alpha=16, dropout=0.05 |
| Batch | per_device=1 |
| Gradient accumulation | 8 |
| Sequence length | 512 |
| Seed | 42 |

## Memory profiling log template

Fill after GPU smoke run:

```text
GPU: ____________
VRAM total: ____ GB
Smoke peak VRAM: ____ GB
Full-run peak VRAM: ____ GB
Tokens/sec (train): ____
OOM events: ____
Notes:
```

Save completed log to `mmc/deliverables/outputs/week09_memory_profile.txt`.

## Packaging

- `scripts/package_for_kaggle.py`
- `notebooks/KAGGLE_SAFE_RUN.md`
- `notebooks/kaggle_runner.ipynb`

## Status

`packaged` — configuration and runner ready; profiling numbers pending free-GPU execution.
