from pathlib import Path
import re

css_path = Path("docs/assets/css/site.css")
css = css_path.read_text()

css = css.replace(
    '''.def-list dt {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--muted);
}''',
    '''.def-list dt {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  letter-spacing: 0.015em;
  text-transform: none;
  color: var(--muted);
}''',
    1,
)

css = css.replace(
    '''.metric .label {
  display: block;
  color: var(--muted);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 500;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-bottom: 0.45rem;
}''',
    '''.metric .label {
  display: block;
  color: var(--muted);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 500;
  letter-spacing: 0.015em;
  text-transform: none;
  margin-bottom: 0.45rem;
}''',
    1,
)
css_path.write_text(css)

for path in Path("docs").rglob("*.html"):
    text = path.read_text()
    updated = re.sub(
        r'<meta name="theme-color" content="#[0-9A-Fa-f]{6}"\s*/?>',
        '<meta name="theme-color" content="#050a08" />',
        text,
    )
    if updated != text:
        path.write_text(updated)
