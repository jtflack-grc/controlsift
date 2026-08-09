"""QLoRA training entrypoint for Gemma 3 1B IT.

Intended to run on Kaggle / Colab with optional GPU extras installed:
  pip install -e ".[gpu]"

This module does not download models in CI.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Optional

from controlsift import CANONICAL_SEED
from controlsift.prompting.templates import build_zero_shot_prompt
from controlsift.training.config import load_yaml_config, resolve_lora_target_modules

REPO_ROOT = Path(__file__).resolve().parents[3]


def _require_gpu_stack():
    try:
        import torch  # noqa: F401
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training  # noqa: F401
        from transformers import (  # noqa: F401
            AutoModelForCausalLM,
            AutoTokenizer,
            BitsAndBytesConfig,
            TrainingArguments,
        )
        from trl import SFTTrainer  # noqa: F401
    except ImportError as exc:
        raise SystemExit(
            "GPU dependencies missing. Install with: pip install -e \".[gpu]\" "
            "on a CUDA machine (Kaggle/Colab)."
        ) from exc


def format_training_example(case: dict[str, Any]) -> str:
    prompt = build_zero_shot_prompt(case)
    target = json.dumps(
        {
            "label": case["label"],
            "rationale": f"Rule-derived label {case['label']} for synthetic evidence.",
        }
    )
    return prompt + "\n" + target


def train_qlora(config_path: Path, *, max_steps: Optional[int] = None) -> dict[str, Any]:
    _require_gpu_stack()
    import torch
    from datasets import Dataset
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        TrainingArguments,
    )
    from trl import SFTTrainer

    from controlsift.evaluation.evaluate import load_jsonl

    cfg = load_yaml_config(config_path)
    seed = int(cfg.get("seed", CANONICAL_SEED))
    train_cases = load_jsonl(REPO_ROOT / cfg["paths"]["train"])
    val_cases = load_jsonl(REPO_ROOT / cfg["paths"]["validation"])

    qcfg = cfg["quantization"]
    compute_dtype = getattr(torch, qcfg.get("bnb_4bit_compute_dtype", "bfloat16"), torch.bfloat16)
    bnb = BitsAndBytesConfig(
        load_in_4bit=bool(qcfg.get("load_in_4bit", True)),
        bnb_4bit_quant_type=qcfg.get("bnb_4bit_quant_type", "nf4"),
        bnb_4bit_use_double_quant=bool(qcfg.get("bnb_4bit_use_double_quant", True)),
        bnb_4bit_compute_dtype=compute_dtype,
    )

    model_id = cfg["model_id"]
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb,
        device_map="auto",
    )
    model = prepare_model_for_kbit_training(model)

    target_modules = cfg.get("lora", {}).get("target_modules") or resolve_lora_target_modules(model)
    lora_cfg = LoraConfig(
        r=int(cfg["lora"]["r"]),
        lora_alpha=int(cfg["lora"]["lora_alpha"]),
        lora_dropout=float(cfg["lora"]["lora_dropout"]),
        bias=cfg["lora"].get("bias", "none"),
        task_type=cfg["lora"].get("task_type", "CAUSAL_LM"),
        target_modules=target_modules,
    )
    model = get_peft_model(model, lora_cfg)

    train_ds = Dataset.from_list(
        [{"text": format_training_example(c)} for c in train_cases]
    )
    val_ds = Dataset.from_list([{"text": format_training_example(c)} for c in val_cases])

    tcfg = cfg["training"]
    out_dir = REPO_ROOT / cfg["paths"]["output_dir"] / "adapter"
    out_dir.mkdir(parents=True, exist_ok=True)

    args_kwargs: dict[str, Any] = dict(
        output_dir=str(out_dir),
        num_train_epochs=float(tcfg.get("num_train_epochs", 3)),
        learning_rate=float(tcfg.get("learning_rate", 2e-4)),
        per_device_train_batch_size=int(tcfg.get("per_device_train_batch_size", 1)),
        per_device_eval_batch_size=int(tcfg.get("per_device_eval_batch_size", 1)),
        gradient_accumulation_steps=int(tcfg.get("gradient_accumulation_steps", 8)),
        logging_steps=int(tcfg.get("logging_steps", 10)),
        eval_strategy=tcfg.get("eval_strategy", "steps"),
        eval_steps=int(tcfg.get("eval_steps", 50)),
        save_strategy=tcfg.get("save_strategy", "steps"),
        save_steps=int(tcfg.get("save_steps", 100)),
        warmup_ratio=float(tcfg.get("warmup_ratio", 0.03)),
        lr_scheduler_type=tcfg.get("lr_scheduler_type", "cosine"),
        seed=seed,
        report_to=[],
        fp16=False,
        bf16=torch.cuda.is_available(),
    )
    if max_steps is not None:
        args_kwargs["max_steps"] = max_steps

    training_args = TrainingArguments(**args_kwargs)

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        processing_class=tokenizer,
    )
    train_result = trainer.train()
    trainer.save_model(str(out_dir))
    tokenizer.save_pretrained(str(out_dir))

    meta = {
        "model_id": model_id,
        "seed": seed,
        "lora_target_modules": target_modules,
        "output_dir": str(out_dir).replace("\\", "/"),
        "train_runtime": float(train_result.metrics.get("train_runtime", 0.0)),
        "train_loss": float(train_result.metrics.get("train_loss", 0.0)),
        "status": "completed",
    }
    meta_path = REPO_ROOT / cfg["paths"]["output_dir"] / "training_meta.json"
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    with meta_path.open("w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")
    return meta


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Train Gemma 3 QLoRA adapter")
    parser.add_argument(
        "--config",
        type=Path,
        default=REPO_ROOT / "configs" / "gemma3_1b_qlora.yaml",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run a tiny max_steps smoke train for environment validation",
    )
    args = parser.parse_args(argv)
    meta = train_qlora(args.config, max_steps=5 if args.smoke else None)
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
