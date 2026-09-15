from pathlib import Path
import re

css_path = Path("docs/assets/css/site.css")
css = css_path.read_text()
old = '''.def-list dt {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--muted);
}'''
new = '''.def-list dt {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  letter-spacing: 0.015em;
  text-transform: none;
  color: var(--muted);
}'''
if old not in css:
    raise SystemExit("def-list dt block not found")
css = css.replace(old, new, 1)
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
