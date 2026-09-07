#!/usr/bin/env python3
"""Evaluate a saved QLoRA adapter on a split (GPU / Kaggle / Colab).

Requires HF access to the base model and a local adapter directory produced by training.
Never prints secrets.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from controlsift import CANONICAL_SEED
from controlsift.evaluation.evaluate import (
    evaluate_predictions,
    load_jsonl,
    save_predictions,
    write_json,
)
from controlsift.evaluation.parser import parse_model_output
from controlsift.prompting.templates import build_zero_shot_prompt

REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_ID = "google/gemma-3-1b-it"

# Allow `python scripts/run_gemma_qlora_eval.py` to import sibling helpers.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _torchao_preflight import ensure_torchao_compatible  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--adapter",
        type=Path,
        default=REPO_ROOT / "results" / "gemma_qlora" / "adapter",
    )
    parser.add_argument(
        "--split",
        choices=["validation", "test", "challenge"],
        default="validation",
    )
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--seed", type=int, default=CANONICAL_SEED)
    args = parser.parse_args()

    try:
        import os

        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise SystemExit('Install GPU extras: pip install -e ".[gpu]"') from exc

    # Fix torchao BEFORE importing peft — peft>=0.16 can ImportError on stale torchao at import.
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
    ensure_torchao_compatible()

    try:
        from peft import PeftModel
    except ImportError as exc:
        msg = str(exc)
        if "torchao" in msg.lower():
            raise SystemExit(
                f"{msg}\n"
                "Fix: re-run Install cell (pip install -U torchao>=0.16), "
                "or: pip uninstall -y torchao"
            ) from exc
        raise SystemExit('Install GPU extras: pip install -e ".[gpu]"') from exc

    if not args.adapter.exists():
        raise SystemExit(
            f"Adapter not found: {args.adapter}. "
            "Train first, or re-Locate only after results/ preserve lands "
            "(stash restores results/gemma_qlora/adapter)."
        )

    cases = load_jsonl(REPO_ROOT / "data" / "processed" / f"{args.split}.jsonl")
    if args.limit:
        cases = cases[: args.limit]

    tokenizer = AutoTokenizer.from_pretrained(args.adapter)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    try:
        from transformers import Gemma3ForCausalLM

        model_cls = Gemma3ForCausalLM
    except ImportError:
        model_cls = AutoModelForCausalLM
    dtype = (
        torch.bfloat16
        if torch.cuda.is_available() and torch.cuda.get_device_capability(0)[0] >= 8
        else torch.float16
    )
    base = model_cls.from_pretrained(
        MODEL_ID,
        device_map={"": 0},
        torch_dtype=dtype,
    )
    try:
        model = PeftModel.from_pretrained(base, str(args.adapter))
    except ImportError as exc:
        msg = str(exc)
        if "torchao" in msg.lower():
            raise SystemExit(
                f"{msg}\n"
                "Fix: re-run Install cell (pip install -U torchao>=0.16), "
                "or: pip uninstall -y torchao"
            ) from exc
        raise
    model.eval()

    pred_rows = []
    device = getattr(model, "device", None)
    if device is None:
        device = next(model.parameters()).device
    for case in cases:
        prompt = build_zero_shot_prompt(case)
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            out = model.generate(
                **inputs,
                max_new_tokens=128,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        text = tokenizer.decode(
            out[0][inputs["input_ids"].shape[-1] :],
            skip_special_tokens=True,
        )
        parsed = parse_model_output(text)
        pred_rows.append(
            {
                "id": case["id"],
                "pred_label": parsed["label"],
                "rationale": parsed.get("rationale", ""),
                "parse_status": parsed.get("parse_status"),
                "split": args.split,
                "raw": (parsed.get("raw") or "")[:2000],
            }
        )

    out_dir = REPO_ROOT / "results" / "gemma_qlora"
    save_predictions(out_dir / f"predictions_{args.split}.jsonl", pred_rows)
    payload = evaluate_predictions(
        cases,
        pred_rows,
        experiment="gemma_qlora",
        model=f"{MODEL_ID}+qlora",
        seed=args.seed,
        run_bootstrap=args.split == "test" and args.limit is None,
    )
    write_json(out_dir / f"metrics_{args.split}.json", payload)
    print(
        json.dumps(
            {
                "ok": True,
                "experiment": "gemma_qlora",
                "split": args.split,
                "n": len(cases),
                "macro_f1": payload["metrics"]["macro_f1"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
