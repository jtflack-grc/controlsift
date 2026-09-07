"""Copy MMC deliverable outputs + notebooks + GDM lab refs into docs/ for static viewing."""

from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

from mmc.labs.build_notebooks import SPECS
from mmc.labs.paths import DOCS_DELIV, MMC, OUT, ROOT, ensure_out

LAB_SOURCES = [
    "week01_ngram.py",
    "week02_bpe.py",
    "week04_mlp.py",
    "week05_diagnostics.py",
    "week06_transformer.py",
    "week07_lora_scaffold.py",
    "week11_comparative.py",
    "sample_corpus.txt",
    "paths.py",
    "run_all.py",
]

EXTRA_FILES = [
    ROOT / "configs" / "gemma3_1b_qlora.yaml",
    ROOT / "notebooks" / "KAGGLE_SAFE_RUN.md",
    MMC / "GDM_LAB_MAP.md",
]


def _copy(src: Path, dest_dir: Path) -> str | None:
    if not src.is_file():
        return None
    dest_dir.mkdir(parents=True, exist_ok=True)
    target = dest_dir / src.name
    shutil.copy2(src, target)
    return str(target)


def _write_source_view(src: Path, dest_dir: Path) -> str | None:
    """HTML wrapper so lab source renders in-browser (not as a download)."""
    if not src.is_file() or src.suffix not in {".py", ".txt", ".yaml", ".md"}:
        return None
    dest_dir.mkdir(parents=True, exist_ok=True)
    target = dest_dir / f"{src.name}.html"
    body = html.escape(src.read_text(encoding="utf-8"))
    rel_to_deliv = Path(*([".."] * len(dest_dir.relative_to(DOCS_DELIV).parts)))
    css = (rel_to_deliv / ".." / ".." / "assets" / "css" / "site.css").as_posix()
    hub = (rel_to_deliv / "index.html").as_posix()
    target.write_text(
        f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(src.name)}</title>
  <link rel="stylesheet" href="{css}" />
  <style>
    pre.source {{
      margin: 1rem 0 0;
      padding: 1rem;
      overflow: auto;
      border: 1px solid var(--line);
      background: var(--panel);
      font-family: var(--font-mono);
      font-size: var(--text-sm);
      line-height: 1.45;
      white-space: pre;
    }}
  </style>
</head>
<body>
  <main>
    <section class="section" style="border-top:0;padding-top:1rem;">
      <div class="page-intro">
        <h2>{html.escape(src.name)}</h2>
        <p><a href="{html.escape(src.name)}">Download raw file</a> · <a href="{hub}">Deliverables hub</a></p>
      </div>
      <pre class="source"><code>{body}</code></pre>
    </section>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )
    return str(target)


def _write_notebook_view(src: Path, dest_dir: Path) -> str | None:
    if not src.is_file() or src.suffix != ".ipynb":
        return None
    dest_dir.mkdir(parents=True, exist_ok=True)
    target = dest_dir / f"{src.name}.html"
    nb = json.loads(src.read_text(encoding="utf-8"))
    parts: list[str] = []
    for i, cell in enumerate(nb.get("cells", []), start=1):
        src_lines = cell.get("source", [])
        text = html.escape("".join(src_lines) if isinstance(src_lines, list) else str(src_lines))
        kind = cell.get("cell_type", "code")
        parts.append(
            f'<article class="nb-cell nb-{html.escape(kind)}">'
            f"<h3>Cell {i} · {html.escape(kind)}</h3>"
            f"<pre class=\"source\"><code>{text}</code></pre></article>"
        )
    rel_to_deliv = Path(*([".."] * len(dest_dir.relative_to(DOCS_DELIV).parts)))
    css = (rel_to_deliv / ".." / ".." / "assets" / "css" / "site.css").as_posix()
    hub = (rel_to_deliv / "index.html").as_posix()
    target.write_text(
        f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(src.name)}</title>
  <link rel="stylesheet" href="{css}" />
  <style>
    .nb-cell {{ margin: 1.25rem 0; padding-top: 0.5rem; border-top: 1px solid var(--line); }}
    .nb-cell h3 {{ font-size: var(--text-sm); opacity: 0.8; }}
    pre.source {{
      margin: 0.5rem 0 0;
      padding: 1rem;
      overflow: auto;
      border: 1px solid var(--line);
      background: var(--panel);
      font-family: var(--font-mono);
      font-size: var(--text-sm);
      line-height: 1.45;
      white-space: pre-wrap;
    }}
  </style>
</head>
<body>
  <main>
    <section class="section" style="border-top:0;padding-top:1rem;">
      <div class="page-intro">
        <h2>{html.escape(src.name)}</h2>
        <p>
          <a href="{html.escape(src.name)}">Download .ipynb</a> ·
          <a href="{hub}">Deliverables hub</a>
        </p>
        <p>Open in Jupyter from repo: <code>jupyter notebook mmc/notebooks/{html.escape(src.name)}</code></p>
      </div>
      {"".join(parts)}
    </section>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )
    return str(target)


def run() -> list[str]:
    ensure_out()
    dest = DOCS_DELIV / "artifacts"
    labs_dest = dest / "labs"
    nb_dest = dest / "notebooks"
    gdm_dest = dest / "gdm"
    dest.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []

    for src in OUT.iterdir():
        if src.name == ".gitkeep":
            continue
        path = _copy(src, dest)
        if path:
            copied.append(path)

    for src in (MMC / "deliverables").glob("week*.md"):
        path = _copy(src, dest)
        if path:
            copied.append(path)
        view = _write_source_view(src, dest)
        if view:
            copied.append(view)

    # Week 3 badge proof + drop-zone readme (if present).
    for pattern in (
        "week03_skill_badge.png",
        "week03_skill_badge.pdf",
        "week03_skill_badge.jpg",
        "README_WEEK03_BADGE.md",
    ):
        path = _copy(OUT / pattern, dest)
        if path:
            copied.append(path)
        src = OUT / pattern
        if src.is_file() and src.suffix == ".md":
            view = _write_source_view(src, dest)
            if view:
                copied.append(view)

    for name in LAB_SOURCES:
        src = MMC / "labs" / name
        path = _copy(src, labs_dest)
        if path:
            copied.append(path)
        view = _write_source_view(src, labs_dest)
        if view:
            copied.append(view)

    for src in EXTRA_FILES:
        path = _copy(src, dest)
        if path:
            copied.append(path)
        view = _write_source_view(src, dest)
        if view:
            copied.append(view)

    for nb in (MMC / "notebooks").glob("week*.ipynb"):
        path = _copy(nb, nb_dest)
        if path:
            copied.append(path)
        view = _write_notebook_view(nb, nb_dest)
        if view:
            copied.append(view)

    # Mirror only the GDM labs referenced by our map (not the whole vendor tree).
    seen: set[str] = set()
    for spec in SPECS:
        for rel in spec["gdm"]:
            if rel in seen:
                continue
            seen.add(rel)
            src = ROOT / rel
            if not src.is_file():
                continue
            parts = Path(rel).parts  # vendor / ai-foundations / course_x / file.ipynb
            course_dir = gdm_dest / parts[2] if len(parts) >= 4 else gdm_dest
            path = _copy(src, course_dir)
            if path:
                copied.append(path)
            view = _write_notebook_view(src, course_dir)
            if view:
                copied.append(view)

    return copied


if __name__ == "__main__":
    for p in run():
        print(p)
