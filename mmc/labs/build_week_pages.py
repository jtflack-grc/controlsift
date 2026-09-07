"""Generate docs/capstone/deliverables/weekXX.html landing pages with artifact links."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from mmc.labs.build_notebooks import SPECS
from mmc.labs.paths import DOCS_DELIV, ROOT

# week number (01) -> MMC notebook + official GDM paths
_NB_BY_WEEK: dict[str, dict] = {}
for _spec in SPECS:
    _num = _spec["file"][4:6]  # weekNN_...
    _NB_BY_WEEK[_num] = _spec

WEEKS: list[dict] = [
    {
        "n": "01",
        "title": "N-gram LM + perplexity",
        "status": "meets",
        "blurb": "Working n-gram text generator with automated perplexity logs.",
        "artifacts": [
            ("Perplexity log (JSON)", "artifacts/week01_perplexity.json"),
            ("Sample generation", "artifacts/week01_sample.txt"),
            ("Lab source", "artifacts/labs/week01_ngram.py.html"),
            ("Sample corpus", "artifacts/labs/sample_corpus.txt.html"),
        ],
    },
    {
        "n": "02",
        "title": "BPE tokenizer + Data Card",
        "status": "meets",
        "blurb": "Custom subword tokenizer, vocabulary export, and Data Card link.",
        "artifacts": [
            ("Summary", "artifacts/week02_summary.json"),
            ("Vocabulary", "artifacts/week02_vocab.json"),
            ("Merges", "artifacts/week02_merges.json"),
            ("Data Card", "../../assurance/data-card.html"),
            ("Lab source", "artifacts/labs/week02_bpe.py.html"),
        ],
    },
    {
        "n": "03",
        "title": "DeepMind Skill Badge",
        "status": "meets",
        "blurb": "Official Train a Small Language Model skill badge proof attached.",
        "artifacts": [
            (
                "Public credential (Skills)",
                "https://www.skills.google/public_profiles/a6a2045d-a94e-4ea5-a1f1-7752f2dab561/badges/26439446",
            ),
            ("Badge screenshot", "artifacts/week03_skill_badge.png"),
            ("Badge evidence record", "artifacts/week03_skill_badge.md.html"),
        ],
    },
    {
        "n": "04",
        "title": "MLP from scratch",
        "status": "meets",
        "blurb": "NumPy MLP classifier with saved weights and loss curve.",
        "artifacts": [
            ("Summary", "artifacts/week04_summary.json"),
            ("Loss curve JSON", "artifacts/week04_loss_curve.json"),
            ("Weights (NPZ)", "artifacts/week04_mlp_weights.npz"),
            ("Lab source", "artifacts/labs/week04_mlp.py.html"),
        ],
    },
    {
        "n": "05",
        "title": "Diagnostics dashboard",
        "status": "meets",
        "blurb": "Overfit / underfit experiments with loss-curve dashboard.",
        "artifacts": [
            ("Dashboard", "week05-dashboard.html"),
            ("Loss curves PNG", "artifacts/week05_loss_curves.png"),
            ("Metrics JSON", "artifacts/week05_metrics.json"),
            ("Lab source", "artifacts/labs/week05_diagnostics.py.html"),
        ],
    },
    {
        "n": "06",
        "title": "Transformer decoder + attention",
        "status": "meets",
        "blurb": "Tiny causal decoder block with attention visualization.",
        "artifacts": [
            ("Attention map PNG", "artifacts/week06_attention.png"),
            ("Summary", "artifacts/week06_summary.json"),
            ("Decoder weights (NPZ)", "artifacts/week06_decoder_weights.npz"),
            ("Lab source", "artifacts/labs/week06_transformer.py.html"),
        ],
    },
    {
        "n": "07",
        "title": "LoRA adapter checkpoint",
        "status": "scaffold / GPU",
        "status_class": "pending-gpu",
        "blurb": "Toy LoRA adapter checkpoint plus path to real Gemma QLoRA outputs.",
        "artifacts": [
            ("Summary", "artifacts/week07_summary.json"),
            ("Toy LoRA adapter (NPZ)", "artifacts/week07_lora_adapter.npz"),
            ("QLoRA config", "artifacts/gemma3_1b_qlora.yaml"),
            ("Lab source", "artifacts/labs/week07_lora_scaffold.py.html"),
        ],
    },
    {
        "n": "08",
        "title": "Alignment & Safety Report",
        "status": "meets",
        "blurb": "Model alignment and safety report (use-alignment; RLHF/DPO non-claims).",
        "artifacts": [
            ("Alignment & Safety Report", "artifacts/week08_alignment_safety_report.md"),
            ("Risk register", "../../assurance/risk-register.html"),
            ("Intended use", "../../assurance/intended-use.html"),
        ],
    },
    {
        "n": "09",
        "title": "Accelerate / memory profiling",
        "status": "packaged",
        "status_class": "pending-gpu",
        "blurb": "Optimized fine-tuning pipeline notes and memory profile template.",
        "artifacts": [
            ("Accelerate notes", "artifacts/week09_accelerate.md"),
            ("Kaggle safe run", "artifacts/KAGGLE_SAFE_RUN.md"),
        ],
    },
    {
        "n": "10",
        "title": "Research proposal & baselines",
        "status": "meets",
        "blurb": "Capstone formulation: problem, Data Card, reproducible classical baselines.",
        "artifacts": [
            ("Research proposal", "artifacts/week10_research_proposal.md"),
            ("Methods", "../methods-evidence.html"),
            ("Results", "../../results.html"),
            ("Data Card", "../../assurance/data-card.html"),
        ],
    },
    {
        "n": "11",
        "title": "Training & benchmarking",
        "status": "partial",
        "status_class": "pending-gpu",
        "blurb": "Comparative analysis harness; Gemma weights pending GPU.",
        "artifacts": [
            ("Training checklist", "artifacts/week11_training_benchmarking.md"),
            ("Comparative analysis JSON", "artifacts/week11_comparative_analysis.json"),
            ("Lab source", "artifacts/labs/week11_comparative.py.html"),
            ("Failure Lab", "../../failure-lab.html"),
            ("QLoRA config", "artifacts/gemma3_1b_qlora.yaml"),
        ],
    },
    {
        "n": "12",
        "title": "Synthesis & defense",
        "status": "partial",
        "status_class": "pending-gpu",
        "blurb": "Paper, GitHub docs, slides, video script, defense Q&A.",
        "artifacts": [
            ("Defense packet", "artifacts/week12_synthesis_defense.md"),
            ("≤8-page report", "../report.html"),
            ("Research paper", "../paper.html"),
            ("Slides", "../slides.html"),
            ("Video script", "../video-script.html"),
        ],
    },
]


def _gemma_test_ready() -> bool:
    """True when public results.json has non-null TEST macro_f1 for all Gemma rungs."""
    path = ROOT / "docs" / "data" / "results.json"
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    experiments = data.get("experiments") or {}
    for key in ("gemma_zero_shot", "gemma_few_shot", "gemma_qlora"):
        row = experiments.get(key) or {}
        if row.get("macro_f1") is None:
            return False
    return True


def _weeks_for_render() -> list[dict]:
    """Apply GPU-complete status from results.json; never invent numeric scores."""
    weeks = deepcopy(WEEKS)
    if not _gemma_test_ready():
        return weeks
    upgrades = {
        "07": {
            "status": "meets",
            "status_class": "",
            "blurb": "Toy LoRA scaffold plus real Gemma QLoRA TEST metrics in public results.",
        },
        "09": {
            "status": "meets",
            "status_class": "",
            "blurb": "Optimized fine-tuning path exercised; Gemma TEST metrics published.",
        },
        "11": {
            "status": "meets",
            "status_class": "",
            "blurb": "Comparative harness complete; Gemma TEST macro F1 loaded from results.json.",
        },
        "12": {
            "status": "partial",
            "status_class": "",
            "blurb": "Paper/slides/report bind to results.json; video recording still manual.",
        },
    }
    for week in weeks:
        patch = upgrades.get(week["n"])
        if not patch:
            continue
        week.update(patch)
        if not week.get("status_class"):
            week.pop("status_class", None)
    return weeks


def _notebook_items(week_n: str) -> list[tuple[str, str]]:
    spec = _NB_BY_WEEK.get(week_n)
    if not spec:
        return []
    items: list[tuple[str, str]] = [
        ("MMC show-work notebook", f"artifacts/notebooks/{spec['file']}.html"),
        ("Download MMC .ipynb", f"artifacts/notebooks/{spec['file']}"),
    ]
    for rel in spec["gdm"]:
        parts = Path(rel).parts
        # vendor/ai-foundations/course_x/file.ipynb
        course, name = parts[2], parts[3]
        items.append((f"Official GDM · {name}", f"artifacts/gdm/{course}/{name}.html"))
    return items


def render(week: dict) -> str:
    status_class = week.get("status_class", "")
    pill = f'status-pill{" " + status_class if status_class else ""}'
    art = list(_notebook_items(week["n"])) + list(week["artifacts"])
    if week["n"] in {"01", "02", "04", "05", "06", "07", "09", "11"}:
        art.append(("GDM ↔ MMC map", "artifacts/GDM_LAB_MAP.md.html"))
    def _li(label: str, href: str) -> str:
        if href.startswith("http://") or href.startswith("https://"):
            return (
                f'        <li><a href="{href}" rel="noopener noreferrer" '
                f'target="_blank">{label}</a></li>'
            )
        return f'        <li><a href="{href}">{label}</a></li>'

    items = "\n".join(_li(label, href) for label, href in art)
    n = week["n"]
    prev_n = f"{int(n) - 1:02d}" if int(n) > 1 else None
    next_n = f"{int(n) + 1:02d}" if int(n) < 12 else None
    nav = []
    if prev_n:
        nav.append(f'<a class="btn btn-secondary" href="week{prev_n}.html">← Week {int(prev_n)}</a>')
    if next_n:
        nav.append(f'<a class="btn btn-secondary" href="week{next_n}.html">Week {int(next_n)} →</a>')
    nav.append('<a class="btn btn-secondary" href="index.html">Deliverables hub</a>')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="color-scheme" content="dark" />
  <meta name="theme-color" content="#000000" />
  <title>Week {int(n)} — {week["title"]}</title>
  <meta name="robots" content="noindex" />
  <link rel="stylesheet" href="../../assets/css/site.css" />
</head>
<body>
  <header class="site-header">
    <nav class="nav" aria-label="Primary">
      <a class="brand" href="../../index.html">ControlSift</a>
      <ul class="nav-links" data-site-nav></ul>
    </nav>
  </header>
  <main>
    <section class="section" style="border-top:0;padding-top:1rem;">
      <nav class="capstone-nav" data-capstone-nav aria-label="Capstone"></nav>
      <div class="page-intro">
        <h2>Week {int(n)} · {week["title"]}</h2>
        <p>{week["blurb"]}</p>
      </div>
      <div class="def-list">
        <div><dt>Status</dt><dd><span class="{pill}">{week["status"]}</span></dd></div>
      </div>
      <h3 style="margin-top:1.5rem;">Artifacts</h3>
      <ul class="findings-list">
{items}
      </ul>
      <div class="cta-row" style="margin-top:1.5rem;">
        {" ".join(nav)}
      </div>
    </section>
  </main>
  <footer class="site-footer"><div class="wrap"><span>Week {int(n)}</span><a href="index.html">Hub</a></div></footer>
  <script src="../../assets/js/nav.js"></script>
  <script src="../../assets/js/capstone-nav.js"></script>
</body>
</html>
"""


def main() -> None:
    DOCS_DELIV.mkdir(parents=True, exist_ok=True)
    weeks = _weeks_for_render()
    ready = _gemma_test_ready()
    print(
        "gemma_test_ready=",
        ready,
        "(week 07/09/11/12 status flips only when results.json has non-null Gemma TEST macro_f1)",
    )
    for week in weeks:
        path = DOCS_DELIV / f"week{week['n']}.html"
        path.write_text(render(week), encoding="utf-8")
        print("wrote", path)


if __name__ == "__main__":
    main()
