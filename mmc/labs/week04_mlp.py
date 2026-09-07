"""Week 4 deliverable: MLP classifier from scratch (NumPy only)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from mmc.labs.paths import ensure_out


def make_moons(n: int = 200, seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n2 = n // 2
    t = rng.uniform(0, np.pi, n2)
    x1 = np.stack([np.cos(t), np.sin(t)], axis=1) + rng.normal(0, 0.08, (n2, 2))
    x2 = np.stack([1 - np.cos(t), 1 - np.sin(t) - 0.5], axis=1) + rng.normal(0, 0.08, (n2, 2))
    x = np.concatenate([x1, x2], axis=0)
    y = np.concatenate([np.zeros(n2), np.ones(n2)])
    idx = rng.permutation(n)
    return x[idx], y[idx]


class MLP:
    def __init__(self, in_dim: int = 2, hidden: int = 16, seed: int = 42) -> None:
        rng = np.random.default_rng(seed)
        self.w1 = rng.normal(0, 0.5, (in_dim, hidden))
        self.b1 = np.zeros(hidden)
        self.w2 = rng.normal(0, 0.5, (hidden, 1))
        self.b2 = np.zeros(1)

    @staticmethod
    def _sigmoid(z: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))

    def forward(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        h = np.tanh(x @ self.w1 + self.b1)
        logits = h @ self.w2 + self.b2
        p = self._sigmoid(logits)
        return h, logits, p

    def fit(self, x: np.ndarray, y: np.ndarray, epochs: int = 400, lr: float = 0.1) -> list[float]:
        y = y.reshape(-1, 1)
        losses: list[float] = []
        n = x.shape[0]
        for _ in range(epochs):
            h, _, p = self.forward(x)
            eps = 1e-9
            loss = float(-np.mean(y * np.log(p + eps) + (1 - y) * np.log(1 - p + eps)))
            losses.append(loss)
            dlogits = (p - y) / n
            dw2 = h.T @ dlogits
            db2 = dlogits.sum(axis=0)
            dh = dlogits @ self.w2.T * (1 - h**2)
            dw1 = x.T @ dh
            db1 = dh.sum(axis=0)
            self.w2 -= lr * dw2
            self.b2 -= lr * db2
            self.w1 -= lr * dw1
            self.b1 -= lr * db1
        return losses

    def predict(self, x: np.ndarray) -> np.ndarray:
        return (self.forward(x)[2] >= 0.5).astype(int).ravel()


def run() -> dict:
    out = ensure_out()
    x, y = make_moons(240)
    split = 180
    mlp = MLP()
    losses = mlp.fit(x[:split], y[:split])
    pred = mlp.predict(x[split:])
    acc = float((pred == y[split:]).mean())
    # persist weights as the "from scratch" artifact
    np.savez(out / "week04_mlp_weights.npz", w1=mlp.w1, b1=mlp.b1, w2=mlp.w2, b2=mlp.b2)
    summary = {
        "deliverable": "week04_mlp_from_scratch",
        "implementation": "numpy",
        "train_size": split,
        "test_accuracy": acc,
        "final_loss": losses[-1],
        "weights": str(out / "week04_mlp_weights.npz"),
    }
    (out / "week04_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out / "week04_loss_curve.json").write_text(json.dumps(losses), encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
