"""Figure generation from machine-readable results (§49)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[3]
LABELS = [
    "SUFFICIENT",
    "PARTIAL",
    "INSUFFICIENT",
    "IRRELEVANT",
    "CONTRADICTORY",
]


def _load(path: Path) -> Optional[dict[str, Any]]:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _macro_f1(exp: str) -> Optional[float]:
    payload = _load(REPO_ROOT / "results" / exp / "metrics_test.json")
    if not payload:
        return None
    return payload.get("metrics", {}).get("macro_f1")


def build_all_figures(figures_dir: Optional[Path] = None) -> list[str]:
    figures_dir = figures_dir or (REPO_ROOT / "reports" / "figures")
    figures_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []

    experiments = [
        "majority",
        "tfidf",
        "gemma_zero_shot",
        "gemma_few_shot",
        "gemma_qlora",
    ]
    scores = [_macro_f1(e) for e in experiments]

    # 1. model comparison
    fig, ax = plt.subplots(figsize=(8, 4))
    xs = np.arange(len(experiments))
    vals = [s if s is not None else 0.0 for s in scores]
    colors = ["#2f5d50" if s is not None else "#b8b0a4" for s in scores]
    ax.bar(xs, vals, color=colors)
    ax.set_xticks(xs)
    ax.set_xticklabels(experiments, rotation=25, ha="right")
    ax.set_ylabel("Macro F1")
    ax.set_ylim(0, 1)
    ax.set_title("Model comparison (null experiments shown as 0 / grey)")
    for i, s in enumerate(scores):
        label = "n/a" if s is None else f"{s:.3f}"
        ax.text(i, vals[i] + 0.02, label, ha="center", fontsize=8)
    fig.tight_layout()
    path = figures_dir / "01_model_comparison.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    written.append(str(path))

    # Prefer TF-IDF for class charts if present, else majority
    source = None
    for exp in ("gemma_qlora", "tfidf", "majority"):
        source = _load(REPO_ROOT / "results" / exp / "metrics_test.json")
        if source and source.get("metrics", {}).get("per_class"):
            break

    if source and source["metrics"].get("per_class"):
        per = source["metrics"]["per_class"]
        f1s = [per[label]["f1"] for label in LABELS]
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(LABELS, f1s, color="#2f5d50")
        ax.set_ylim(0, 1)
        ax.set_title(f"Per-class F1 ({source.get('experiment')})")
        ax.tick_params(axis="x", rotation=20)
        fig.tight_layout()
        path = figures_dir / "02_per_class_f1.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        written.append(str(path))

        cm = np.array(source["metrics"]["confusion_matrix"], dtype=float)
        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(cm, cmap="Greens")
        ax.set_xticks(range(len(LABELS)))
        ax.set_yticks(range(len(LABELS)))
        ax.set_xticklabels(LABELS, rotation=45, ha="right", fontsize=7)
        ax.set_yticklabels(LABELS, fontsize=7)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("True")
        ax.set_title("Confusion matrix")
        fig.colorbar(im, ax=ax, fraction=0.046)
        fig.tight_layout()
        path = figures_dir / "03_confusion_matrix.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        written.append(str(path))

        cmn = np.array(source["metrics"]["confusion_matrix_normalized"], dtype=float)
        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(cmn, cmap="Greens", vmin=0, vmax=1)
        ax.set_xticks(range(len(LABELS)))
        ax.set_yticks(range(len(LABELS)))
        ax.set_xticklabels(LABELS, rotation=45, ha="right", fontsize=7)
        ax.set_yticklabels(LABELS, fontsize=7)
        ax.set_title("Normalized confusion matrix")
        fig.colorbar(im, ax=ax, fraction=0.046)
        fig.tight_layout()
        path = figures_dir / "04_confusion_matrix_normalized.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        written.append(str(path))

    # Placeholder stubs for figures that need full LLM runs / learning curves
    stubs = [
        ("05_learning_curve.png", "Learning curve (pending scaling runs)"),
        ("06_failure_type_performance.png", "Performance by failure type (pending)"),
        ("07_domain_performance.png", "Performance by domain (see slice JSON)"),
        ("08_train_val_loss.png", "Training / validation loss (pending QLoRA)"),
        ("09_baseline_vs_tuned.png", "Baseline vs tuned (pending QLoRA)"),
        ("10_challenge_comparison.png", "Challenge-set comparison"),
    ]
    for filename, title in stubs:
        # Prefer real challenge comparison when available
        if filename == "10_challenge_comparison.png":
            chal_scores = []
            for exp in experiments:
                p = _load(REPO_ROOT / "results" / exp / "metrics_challenge.json")
                chal_scores.append(
                    None if not p else p.get("metrics", {}).get("macro_f1")
                )
            if any(s is not None for s in chal_scores):
                fig, ax = plt.subplots(figsize=(8, 4))
                vals = [s if s is not None else 0.0 for s in chal_scores]
                ax.bar(experiments, vals, color="#2f5d50")
                ax.set_ylim(0, 1)
                ax.tick_params(axis="x", rotation=25)
                ax.set_title("Challenge-set macro F1")
                fig.tight_layout()
                path = figures_dir / filename
                fig.savefig(path, dpi=150)
                plt.close(fig)
                written.append(str(path))
                continue

        if filename == "07_domain_performance.png" and source and source.get("slices"):
            domain = source["slices"].get("control_domain", {})
            if domain:
                keys = sorted(domain.keys())
                vals = [domain[k]["macro_f1"] for k in keys]
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.bar(keys, vals, color="#2f5d50")
                ax.set_ylim(0, 1)
                ax.tick_params(axis="x", rotation=45)
                ax.set_title("Macro F1 by control domain")
                fig.tight_layout()
                path = figures_dir / filename
                fig.savefig(path, dpi=150)
                plt.close(fig)
                written.append(str(path))
                continue

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.axis("off")
        ax.text(0.5, 0.5, title, ha="center", va="center", fontsize=11)
        ax.set_title("Pending real experiment artifacts — not fabricated metrics")
        fig.tight_layout()
        path = figures_dir / filename
        fig.savefig(path, dpi=120)
        plt.close(fig)
        written.append(str(path))

    return written
