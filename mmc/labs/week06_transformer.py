"""Week 6 deliverable: tiny Transformer decoder block + attention visualization."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from mmc.labs.paths import DOCS_DELIV, ensure_out


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    x = x - x.max(axis=axis, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)


class TinyDecoderBlock:
    """Single-head self-attention + FFN (NumPy)."""

    def __init__(self, d_model: int = 32, seed: int = 42) -> None:
        rng = np.random.default_rng(seed)
        self.d_model = d_model
        scale = 0.2
        self.wq = rng.normal(0, scale, (d_model, d_model))
        self.wk = rng.normal(0, scale, (d_model, d_model))
        self.wv = rng.normal(0, scale, (d_model, d_model))
        self.wo = rng.normal(0, scale, (d_model, d_model))
        self.w1 = rng.normal(0, scale, (d_model, 4 * d_model))
        self.w2 = rng.normal(0, scale, (4 * d_model, d_model))

    def attention(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        # x: [T, D]
        q = x @ self.wq
        k = x @ self.wk
        v = x @ self.wv
        scores = (q @ k.T) / np.sqrt(self.d_model)
        # causal mask
        t = x.shape[0]
        mask = np.triu(np.ones((t, t)), k=1) * -1e9
        weights = softmax(scores + mask, axis=-1)
        ctx = weights @ v
        return ctx @ self.wo, weights

    def forward(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        attn, weights = self.attention(x)
        h = x + attn
        ff = np.tanh(h @ self.w1) @ self.w2
        return h + ff, weights


def run() -> dict:
    out = ensure_out()
    docs = DOCS_DELIV
    docs.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(42)
    t, d = 12, 32
    # pretend token embeddings
    x = rng.normal(0, 0.5, (t, d))
    block = TinyDecoderBlock(d_model=d)
    y, weights = block.forward(x)

    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(weights, cmap="viridis")
    ax.set_title("Causal self-attention weights")
    ax.set_xlabel("key")
    ax.set_ylabel("query")
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    png = out / "week06_attention.png"
    fig.savefig(png, dpi=120)
    plt.close(fig)
    (docs / "week06_attention.png").write_bytes(png.read_bytes())

    np.savez(out / "week06_decoder_weights.npz", wq=block.wq, wk=block.wk, wv=block.wv, wo=block.wo)
    summary = {
        "deliverable": "week06_transformer_decoder",
        "seq_len": t,
        "d_model": d,
        "output_norm": float(np.linalg.norm(y)),
        "attention_png": str(png),
        "causal": True,
        "heads": 1,
    }
    (out / "week06_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
