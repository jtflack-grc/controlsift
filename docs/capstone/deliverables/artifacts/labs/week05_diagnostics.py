"""Week 5 deliverable: diagnostics dashboard (loss curves + metrics HTML)."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from mmc.labs.paths import DOCS_DELIV, ensure_out
from mmc.labs.week04_mlp import MLP, make_moons


def run() -> dict:
    out = ensure_out()
    docs = DOCS_DELIV
    docs.mkdir(parents=True, exist_ok=True)

    x, y = make_moons(300)
    # underfit: tiny hidden + few epochs
    under = MLP(hidden=2, seed=0)
    under_losses = under.fit(x[:200], y[:200], epochs=40, lr=0.05)
    under_acc = float((under.predict(x[200:]) == y[200:]).mean())

    # overfit-prone: larger net, no early stop, tiny train
    over = MLP(hidden=64, seed=1)
    over_losses = over.fit(x[:40], y[:40], epochs=500, lr=0.2)
    over_acc = float((over.predict(x[200:]) == y[200:]).mean())

    # healthy
    ok = MLP(hidden=16, seed=42)
    ok_losses = ok.fit(x[:200], y[:200], epochs=300, lr=0.1)
    ok_acc = float((ok.predict(x[200:]) == y[200:]).mean())

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(under_losses, label=f"underfit (acc={under_acc:.2f})")
    ax.plot(over_losses, label=f"overfit-prone (acc={over_acc:.2f})")
    ax.plot(ok_losses, label=f"regular run (acc={ok_acc:.2f})")
    ax.set_xlabel("epoch")
    ax.set_ylabel("loss")
    ax.set_title("Week 5 — training dynamics diagnostics")
    ax.legend()
    fig.tight_layout()
    png = out / "week05_loss_curves.png"
    fig.savefig(png, dpi=120)
    plt.close(fig)

    # copy into docs for the dashboard
    docs_png = docs / "week05_loss_curves.png"
    docs_png.write_bytes(png.read_bytes())

    metrics = {
        "deliverable": "week05_diagnostics_dashboard",
        "underfit_test_acc": under_acc,
        "overfit_prone_test_acc": over_acc,
        "healthy_test_acc": ok_acc,
        "notes": [
            "Underfit: capacity too small / too few epochs.",
            "Overfit-prone: tiny train set + high capacity → train loss collapses, test weaker.",
            "Healthy: moderate capacity and train size.",
        ],
    }
    (out / "week05_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>Week 5 Diagnostics</title>
<link rel="stylesheet" href="../../assets/css/site.css"/></head>
<body>
<header class="site-header"><nav class="nav"><a class="brand" href="../../index.html">ControlSift</a>
<ul class="nav-links" data-site-nav></ul></nav></header>
<main><section class="section" style="border-top:0;padding-top:1rem;">
<nav class="capstone-nav" data-capstone-nav></nav>
<div class="page-intro"><h2>Week 5 · Diagnostics dashboard</h2>
<p>Interactive-enough static dashboard for overfitting / underfitting experiments (handbook deliverable).</p></div>
<img src="week05_loss_curves.png" alt="Loss curves" style="max-width:100%;border:1px solid var(--line);"/>
<pre style="margin-top:1rem;font-family:var(--font-mono);font-size:var(--text-sm);overflow:auto;">{json.dumps(metrics, indent=2)}</pre>
<p><a href="index.html">← Deliverables hub</a></p>
</section></main>
<script src="../../assets/js/nav.js"></script>
<script src="../../assets/js/capstone-nav.js"></script>
</body></html>
"""
    (docs / "week05-dashboard.html").write_text(html, encoding="utf-8")
    metrics["dashboard"] = "docs/capstone/deliverables/week05-dashboard.html"
    return metrics


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
