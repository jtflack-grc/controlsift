from pathlib import Path

css_path = Path("docs/assets/css/site.css")
css = css_path.read_text()
css = css.replace("--text-xs: 0.72rem;", "--text-xs: 0.78rem;")
css = css.replace(
    '''.callout strong {
  display: block;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 0.45rem;
}''',
    '''.callout strong {
  display: block;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  letter-spacing: 0.02em;
  color: var(--accent);
  margin-bottom: 0.45rem;
}''',
)
css_path.write_text(css)

cap = Path("docs/capstone/index.html")
text = cap.read_text()
text = text.replace("letter-spacing:.06em;text-transform:none", "letter-spacing:.02em;text-transform:none")
cap.write_text(text)

sources = Path("docs/capstone/research-sources.html")
text = sources.read_text()
text = text.replace("letter-spacing: .055em;", "letter-spacing: .02em;")
text = text.replace("letter-spacing: .05em;", "letter-spacing: .02em;")
sources.write_text(text)
