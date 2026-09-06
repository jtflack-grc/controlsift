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
    import os

    # Kaggle T4x2: keep QLoRA on one GPU. device_map="auto" + Trainer DataParallel crashes.
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")

    import torch
    from datasets import Dataset
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    import dataclasses
    import inspect
    import re

    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        TrainingArguments,
    )
    from trl import SFTTrainer

    try:
        from trl import SFTConfig  # preferred on modern TRL (inherits TrainingArguments)
    except ImportError:  # pragma: no cover - older TRL
        SFTConfig = None

    from controlsift.evaluation.evaluate import load_jsonl

    cfg = load_yaml_config(config_path)
    seed = int(cfg.get("seed", CANONICAL_SEED))
    train_cases = load_jsonl(REPO_ROOT / cfg["paths"]["train"])
    val_cases = load_jsonl(REPO_ROOT / cfg["paths"]["validation"])
    if max_steps is not None:
        # Tiny smoke: keep wall-clock short.
        train_cases = train_cases[: max(8, max_steps * 2)]
        val_cases = val_cases[:8]

    qcfg = cfg["quantization"]
    # T4 (sm 7.5): no bf16 AMP; fp16 GradScaler also crashes if any grads are bf16.
    # Policy: Ampere+ (sm>=8) → bf16 AMP; older GPUs → no AMP + float16 bnb compute.
    use_bf16 = torch.cuda.is_available() and torch.cuda.get_device_capability(0)[0] >= 8
    use_fp16_amp = False
    compute_dtype = torch.bfloat16 if use_bf16 else torch.float16
    requested = qcfg.get("bnb_4bit_compute_dtype", "bfloat16")
    if requested == "float16" or not use_bf16:
        compute_dtype = torch.float16
    elif requested == "bfloat16" and use_bf16:
        compute_dtype = torch.bfloat16
    print(
        "precision:",
        {
            "sm": torch.cuda.get_device_capability(0) if torch.cuda.is_available() else None,
            "compute_dtype": str(compute_dtype),
            "bf16_amp": use_bf16,
            "fp16_amp": use_fp16_amp,
        },
    )
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

    try:
        from transformers import Gemma3ForCausalLM

        model_cls = Gemma3ForCausalLM
    except ImportError:
        model_cls = AutoModelForCausalLM
    model = model_cls.from_pretrained(
        model_id,
        quantization_config=bnb,
        device_map={"": 0},
        torch_dtype=compute_dtype,
    )
    try:
        model = prepare_model_for_kbit_training(
            model,
            use_gradient_checkpointing=True,
        )
    except TypeError:
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
    # Gemma 3 may leave trainable tensors in bf16; T4 GradScaler cannot unscale those.
    for _name, param in model.named_parameters():
        if param.requires_grad and param.dtype == torch.bfloat16:
            param.data = param.data.to(torch.float32)

    train_ds = Dataset.from_list(
        [{"text": format_training_example(c)} for c in train_cases]
    )
    val_ds = Dataset.from_list([{"text": format_training_example(c)} for c in val_cases])

    tcfg = cfg["training"]
    out_dir = REPO_ROOT / cfg["paths"]["output_dir"] / "adapter"
    out_dir.mkdir(parents=True, exist_ok=True)

    max_seq = int(tcfg.get("max_seq_length", 512))
    args_kwargs: dict[str, Any] = dict(
        output_dir=str(out_dir),
        num_train_epochs=float(tcfg.get("num_train_epochs", 3)),
        learning_rate=float(tcfg.get("learning_rate", 2e-4)),
        per_device_train_batch_size=int(tcfg.get("per_device_train_batch_size", 1)),
        per_device_eval_batch_size=int(tcfg.get("per_device_eval_batch_size", 1)),
        gradient_accumulation_steps=int(tcfg.get("gradient_accumulation_steps", 8)),
        logging_steps=int(tcfg.get("logging_steps", 10)),
        eval_strategy=tcfg.get("eval_strategy", "steps"),
        evaluation_strategy=tcfg.get("eval_strategy", "steps"),  # older transformers alias
        eval_steps=int(tcfg.get("eval_steps", 50)),
        save_strategy=tcfg.get("save_strategy", "steps"),
        save_steps=int(tcfg.get("save_steps", 100)),
        warmup_ratio=float(tcfg.get("warmup_ratio", 0.03)),
        warmup_steps=0,
        lr_scheduler_type=tcfg.get("lr_scheduler_type", "cosine"),
        seed=seed,
        report_to=[],
        fp16=use_fp16_amp,
        bf16=use_bf16,
        remove_unused_columns=False,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        # Modern TRL wants these on SFTConfig, not SFTTrainer(...).
        dataset_text_field="text",
        packing=False,
        max_seq_length=max_seq,
        max_length=max_seq,
    )
    eval_dataset = val_ds
    if max_steps is not None:
        args_kwargs["max_steps"] = max_steps
        args_kwargs["eval_strategy"] = "no"
        args_kwargs["evaluation_strategy"] = "no"
        args_kwargs["save_strategy"] = "no"
        args_kwargs["logging_steps"] = 1
        eval_dataset = None

    ArgsCls = SFTConfig if SFTConfig is not None else TrainingArguments

    def _accepted_names(cls: type) -> set[str]:
        names: set[str] = set()
        try:
            names.update(
                f.name
                for f in dataclasses.fields(cls)  # type: ignore[arg-type]
                if f.init
            )
        except (TypeError, ValueError):
            pass
        try:
            for name, param in inspect.signature(cls.__init__).parameters.items():
                if name in {"self", "args", "kwargs"}:
                    continue
                if param.kind in (
                    inspect.Parameter.VAR_POSITIONAL,
                    inspect.Parameter.VAR_KEYWORD,
                ):
                    continue
                names.add(name)
        except (TypeError, ValueError):
            pass
        return names

    def _reconcile_aliases(filtered: dict[str, Any], accepted: set[str]) -> dict[str, Any]:
        out = dict(filtered)
        if "eval_strategy" in out and "evaluation_strategy" in out:
            if "eval_strategy" in accepted and "evaluation_strategy" not in accepted:
                out.pop("evaluation_strategy", None)
            elif "evaluation_strategy" in accepted and "eval_strategy" not in accepted:
                out.pop("eval_strategy", None)
            else:
                out.pop("evaluation_strategy", None)
        if "max_seq_length" in out and "max_length" in out:
            if "max_seq_length" in accepted and "max_length" not in accepted:
                out.pop("max_length", None)
            elif "max_length" in accepted and "max_seq_length" not in accepted:
                out.pop("max_seq_length", None)
            else:
                # Prefer max_length on newest TRL; keep max_seq_length on older.
                if "max_length" in accepted:
                    out.pop("max_seq_length", None)
                else:
                    out.pop("max_length", None)
        if "warmup_ratio" not in out and "warmup_steps" in accepted:
            out["warmup_steps"] = int(args_kwargs.get("warmup_steps", 0))
        return out

    def _build_args(cls: type, raw: dict[str, Any]) -> Any:
        accepted = _accepted_names(cls)
        # If introspection fails (only **kwargs), pass everything and peel on TypeError.
        filtered = dict(raw) if not accepted else {k: v for k, v in raw.items() if k in accepted}
        filtered = _reconcile_aliases(filtered, accepted or set(filtered))
        pending = dict(filtered)
        while True:
            try:
                print(f"{cls.__name__} keys:", sorted(pending.keys()))
                return cls(**pending)
            except TypeError as exc:
                match = re.search(r"unexpected keyword argument '([^']+)'", str(exc))
                if not match:
                    raise
                bad = match.group(1)
                if bad not in pending:
                    raise
                print(f"Dropping unsupported {cls.__name__} kwarg: {bad}")
                pending.pop(bad)
                if bad == "warmup_ratio":
                    pending.setdefault("warmup_steps", 0)

    training_args = _build_args(ArgsCls, args_kwargs)

    trainer_kwargs: dict[str, Any] = dict(
        model=model,
        args=training_args,
        train_dataset=train_ds,
    )
    if eval_dataset is not None:
        trainer_kwargs["eval_dataset"] = eval_dataset

    # TRL API shifted across versions (tokenizer vs processing_class; SFT fields on config).
    sig = inspect.signature(SFTTrainer.__init__)
    params = sig.parameters
    if "processing_class" in params:
        trainer_kwargs["processing_class"] = tokenizer
    elif "tokenizer" in params:
        trainer_kwargs["tokenizer"] = tokenizer
    # Only pass SFT fields on the trainer when the installed TRL still accepts them.
    if "dataset_text_field" in params:
        trainer_kwargs["dataset_text_field"] = "text"
    if "max_seq_length" in params:
        trainer_kwargs["max_seq_length"] = max_seq
    elif "max_length" in params:
        trainer_kwargs["max_length"] = max_seq
    if "packing" in params:
        trainer_kwargs["packing"] = False

    trainer = SFTTrainer(**trainer_kwargs)
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
