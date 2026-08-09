#!/usr/bin/env python3
"""Run Gemma zero-shot / few-shot baselines on GPU (Kaggle/Colab).

Usage:
  python scripts/run_gemma_baseline.py --mode zero_shot --split validation --limit 8
  python scripts/run_gemma_baseline.py --mode few_shot --split test

Does not run in CI. Requires: pip install -e ".[gpu]" and HF access to Gemma.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from controlsift import CANONICAL_SEED
from controlsift.evaluation.evaluate import (
    evaluate_predictions,
    load_jsonl,
    save_predictions,
    write_json,
)
from controlsift.evaluation.parser import parse_model_output
from controlsift.prompting.templates import (
    build_few_shot_prompt,
    build_zero_shot_prompt,
    select_few_shot_examples,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_ID = "google/gemma-3-1b-it"


def _load_model():
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise SystemExit('Install GPU extras: pip install -e ".[gpu]"') from exc

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        device_map="auto",
        torch_dtype=getattr(torch, "bfloat16", torch.float16),
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer, model


def generate(tokenizer, model, prompt: str, max_new_tokens: int = 128) -> str:
    import torch

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            temperature=None,
            pad_token_id=tokenizer.eos_token_id,
        )
    text = tokenizer.decode(out[0][inputs["input_ids"].shape[-1] :], skip_special_tokens=True)
    return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["zero_shot", "few_shot"], required=True)
    parser.add_argument(
        "--split",
        choices=["validation", "test", "challenge"],
        default="validation",
    )
    parser.add_argument("--limit", type=int, default=None, help="Optional cap for smoke tests")
    parser.add_argument("--seed", type=int, default=CANONICAL_SEED)
    args = parser.parse_args()

    train = load_jsonl(REPO_ROOT / "data" / "processed" / "train.jsonl")
    val = load_jsonl(REPO_ROOT / "data" / "processed" / "validation.jsonl")
    cases = load_jsonl(REPO_ROOT / "data" / "processed" / f"{args.split}.jsonl")
    if args.limit:
        cases = cases[: args.limit]

    examples = select_few_shot_examples(train + val) if args.mode == "few_shot" else []
    tokenizer, model = _load_model()

    pred_rows = []
    for case in cases:
        prompt = (
            build_few_shot_prompt(case, examples)
            if args.mode == "few_shot"
            else build_zero_shot_prompt(case)
        )
        raw = generate(tokenizer, model, prompt)
        parsed = parse_model_output(raw)
        pred_rows.append(
            {
                "id": case["id"],
                "pred_label": parsed["label"],
                "rationale": parsed.get("rationale", ""),
                "parse_status": parsed.get("parse_status"),
                "split": args.split,
                "raw": parsed.get("raw", "")[:2000],
            }
        )

    exp = "gemma_zero_shot" if args.mode == "zero_shot" else "gemma_few_shot"
    out_dir = REPO_ROOT / "results" / exp
    save_predictions(out_dir / f"predictions_{args.split}.jsonl", pred_rows)
    payload = evaluate_predictions(
        cases,
        pred_rows,
        experiment=exp,
        model=MODEL_ID,
        seed=args.seed,
        run_bootstrap=args.split == "test" and args.limit is None,
    )
    write_json(out_dir / f"metrics_{args.split}.json", payload)
    print(json.dumps({"ok": True, "experiment": exp, "macro_f1": payload["metrics"]["macro_f1"]}, indent=2))


if __name__ == "__main__":
    main()
