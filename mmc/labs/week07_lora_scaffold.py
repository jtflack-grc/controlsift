"""Week 7 deliverable: LoRA adapter checkpoint scaffold (+ path for real Gemma QLoRA)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from mmc.labs.paths import ensure_out


def run() -> dict:
    out = ensure_out()
    rng = np.random.default_rng(42)
    # Educational LoRA factors for a toy weight matrix (simulates ΔW = A @ B)
    d, r = 64, 8
    a = rng.normal(0, 0.02, (d, r))
    b = rng.normal(0, 0.02, (r, d))
    delta = a @ b
    path = out / "week07_lora_adapter.npz"
    np.savez(path, lora_A=a, lora_B=b, delta_w=delta, rank=r)
    summary = {
        "deliverable": "week07_lora_adapter_checkpoint",
        "status": "scaffold_complete_gpu_pending_for_gemma",
        "toy_adapter": str(path),
        "rank": r,
        "delta_frobenius": float(np.linalg.norm(delta)),
        "production_path": {
            "config": "configs/gemma3_1b_qlora.yaml",
            "train_script": "scripts/run_gemma_qlora_eval.py",
            "expected_output_dir": "results/gemma_qlora/",
            "note": "Replace toy adapter with real PEFT adapter after Kaggle/HF run.",
        },
        "formula": "delta_W = A @ B  (LoRA)",
    }
    (out / "week07_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
