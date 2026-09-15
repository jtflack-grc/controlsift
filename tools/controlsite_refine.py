from pathlib import Path
import re

css_path = Path("docs/assets/css/site.css")
css = css_path.read_text()

css = css.replace("--bg: #07100c;", "--bg: #050a08;")
css = css.replace(
    '--font-display: "IBM Plex Mono", monospace;',
    '--font-display: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif;',
)

font_selector_old = '''body,
button,
input,
select,
textarea,
.nav,
a,
p,
li,
h1, h2, h3, h4, h5, h6 {
  font-family: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif !important;
}'''
font_selector_new = '''body,
button,
input,
select,
textarea,
a,
p,
li,
h1, h2, h3, h4, h5, h6,
table,
th,
td,
summary,
details,
dialog,
label,
dl,
dt,
dd,
figure,
figcaption,
blockquote {
  font-family: var(--font-sans) !important;
}'''
if font_selector_old not in css:
    raise SystemExit("Base IBM Plex selector block not found")
css = css.replace(font_selector_old, font_selector_new, 1)

body_pattern = re.compile(
    r'''body \{\n  margin: 0;\n  min-height: 100vh;.*?\n\}\n\nbody::before \{\n  display: none;\n\}''',
    re.S,
)
body_new = '''body {
  margin: 0;
  min-height: 100vh;
  color: var(--fg);
  background: var(--bg);
  font-family: var(--font-sans) !important;
  font-size: var(--text-md);
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}

/* Portfolio-family signal field: one-axis phosphor scanlines, not a decorative grid. */
body::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(rgba(127, 255, 178, 0.018) 1px, transparent 1px);
  background-size: 100% 4px;
  z-index: 20;
}'''
css, n = body_pattern.subn(body_new, css, count=1)
if n != 1:
    raise SystemExit(f"Body/background block replacement count: {n}")

css = css.replace(
    "background: rgba(7, 16, 12, 0.94);",
    "background: rgba(5, 10, 8, 0.88);",
)

hero_before = re.compile(r'''\.hero::before \{.*?\n\}''', re.S)
css, n = hero_before.subn('''.hero::before {
  display: none;
}''', css, count=1)
if n != 1:
    raise SystemExit("Hero glow block not found")

css = css.replace(
    '''  background:
    linear-gradient(165deg, rgba(127, 255, 178, 0.06), transparent 55%),
    var(--panel);''',
    "  background: var(--panel);",
    1,
)
css = css.replace(
    '''  background:
    linear-gradient(165deg, rgba(127, 255, 178, 0.14), transparent 50%),
    #0a1510;''',
    "  background: #0a1510;",
    1,
)
css = css.replace(
    "  box-shadow: 0 0 0 1px rgba(127, 255, 178, 0.25), 0 24px 64px rgba(0, 0, 0, 0.55);",
    "  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.55);",
    1,
)

css = css.replace(
    "  text-transform: uppercase;\n  animation: rise 1s ease 0.2s forwards;",
    "  animation: rise 1s ease 0.2s forwards;",
    1,
)
css = css.replace(
    '''#welcome-modal .welcome-modal__note {
  margin: 0 0 1rem;
  font-family: "IBM Plex Mono", monospace !important;
  font-size: 0.72rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: #38e881 !important;
}''',
    '''#welcome-modal .welcome-modal__note {
  margin: 0 0 1rem;
  font-family: var(--font-mono) !important;
  font-size: 0.72rem;
  letter-spacing: 0.02em;
  color: #38e881 !important;
}''',
    1,
)

css = css.replace(
    '''  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;''',
    '''  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 500;''',
    1,
)

css = css.replace(
    '''  background: #050605;
  font-family: var(--font-mono);''',
    '''  background: var(--panel);
  font-family: var(--font-mono);''',
    1,
)

css = css.replace(
    '''  text-transform: uppercase;
}

.assurance-nav a {''',
    '''  text-transform: none;
}

.assurance-nav a {''',
    1,
)
css = css.replace(
    '''  text-transform: uppercase;
  list-style: none;
}

.capstone-menu summary::-webkit-details-marker''',
    '''  text-transform: none;
  list-style: none;
}

.capstone-menu summary::-webkit-details-marker''',
    1,
)
css = css.replace('content: " â–¾";', 'content: " +";')
css = css.replace('content: " â–´";', 'content: " −";')
css = css.replace(
    '''  text-transform: uppercase;
}

.curriculum-jump a {''',
    '''  text-transform: none;
}

.curriculum-jump a {''',
    1,
)

orientation = '''

.orientation-note {
  margin: 0 0 1rem;
  padding: 0.9rem 1rem;
  border: 1px solid var(--line);
  background: var(--panel);
  color: #c8e6d2;
  font-size: 0.94rem;
  line-height: 1.5;
}

.orientation-note p { margin: 0 0 0.45rem !important; }
.orientation-note p:last-child { margin-bottom: 0 !important; }
'''
marker = "\n.cta-row {"
if ".orientation-note {" not in css:
    css = css.replace(marker, orientation + marker, 1)

mono_override = '''

code,
pre,
kbd,
samp,
.brand,
.hero-brand,
.hero-note,
.meta-strip,
.metric .label,
.metric .value,
.tag,
.control-block,
.ladder .step,
.ladder .state,
.compare-grid h3,
.compare-grid .score,
.bar-row .name,
.bar-row .val,
.figure-frame figcaption,
.receipts .id,
.callout strong,
.assurance-nav,
.capstone-menu summary,
.capstone-menu-title,
.course-kicker,
.topic-map > h4,
.topic-map .meet,
.def-list dt,
.status-pill,
.integrity-grid .mark,
.paper-meta,
.paper-abstract h2,
.paper-toc h3 {
  font-family: var(--font-mono) !important;
}
'''
reduced_marker = "\n@media (prefers-reduced-motion: reduce) {"
if "paper-abstract h2," not in css:
    css = css.replace(reduced_marker, mono_override + reduced_marker, 1)

css = css.replace(".paper-abstract h3 {", ".paper-abstract h2 {")
css_path.write_text(css)

home = Path("docs/index.html")
text = home.read_text()
text, n = re.subn(r"\n  <style>.*?</style>", "", text, count=1, flags=re.S)
if n != 1:
    raise SystemExit("Homepage inline style block not found")
text = re.sub(r"<body[^>]*>", "<body>", text, count=1)
text = text.replace(
    ' class="hero welcome-door" aria-label="Welcome" style="opacity:1!important;visibility:visible!important;display:block!important;"',
    ' class="hero welcome-door" aria-label="Welcome"',
)
text = re.sub(r' style="[^"]*!important;[^"]*"', "", text)
home.write_text(text)

cap = Path("docs/capstone/index.html")
text = cap.read_text()
text = text.replace(
    "background:linear-gradient(145deg,rgba(127,255,178,.08),transparent 58%),var(--panel)",
    "background:var(--panel)",
)
text = text.replace("text-transform:uppercase", "text-transform:none")
for label in [
    "Final presentation",
    "01 / Submission essentials",
    "02 / Research story",
    "03 / Implementation and responsible research",
    "04 / Program alignment and learning record",
]:
    text = text.replace(f'<p class="hub-kicker">{label}</p>', "")
cap.write_text(text)

sources = Path("docs/capstone/research-sources.html")
text = sources.read_text()
text = text.replace(
    "background: linear-gradient(155deg, rgba(127,255,178,.055), transparent 56%), var(--panel);",
    "background: var(--panel);",
)
text = text.replace("text-transform: uppercase;", "text-transform: none;")
sources.write_text(text)

paper = Path("docs/capstone/paper.html")
text = paper.read_text().replace("<h3>Abstract</h3>", "<h2>Abstract</h2>", 1)
paper.write_text(text)

report = Path("docs/capstone/report.html")
text = report.read_text().replace(
    "body { background: #fff; color: #111; font-size: 10.5pt; line-height: 1.35; }",
    "body { background: transparent; color: #111; font-size: 10.5pt; line-height: 1.35; }",
)
report.write_text(text)

for path in Path("docs").rglob("*.html"):
    text = path.read_text()
    updated = re.sub(r"site\.css\?v=\d+", "site.css?v=2026091501", text)
    if updated != text:
        path.write_text(updated)

design = Path("docs/DESIGN.md")
text = design.read_text()
text = text.replace(
    "OLED-first research surface. True black canvas for emissive displays. Clinical, forensic, receipt-driven - not SaaS launch energy.",
    "Portfolio-family research surface. Near-black green canvas with the same restrained horizontal phosphor scanline field as the main portfolio. Clinical, forensic, receipt-driven - not SaaS launch energy.",
)
text = text.replace("| `--bg` | `#000000` | Page canvas (OLED intentional) |", "| `--bg` | `#050a08` | Portfolio-aligned near-black canvas |")
text = text.replace("| `--fg` | `#e7e9e4` | Primary text |", "| `--fg` | `#e8f4ec` | Primary text |")
text = text.replace("| `--muted` | `#9aa39a` | Secondary text |", "| `--muted` | `#91aa9b` | Secondary text |")
text = text.replace("| `--line` | `#1a1d1a` | Hairlines |", "| `--line` | `rgba(105, 255, 164, 0.16)` | Hairlines |")
text = text.replace("| `--panel` | `#070807` | Recessed panels (near-black, not gray card) |", "| `--panel` | `#09110d` | Recessed panels |")
text = text.replace("| `--accent` | `#d2f27a` | Signal / primary actions |", "| `--accent` | `#7fffb2` | Signal / primary actions |")
text = text.replace("| `--accent-ink` | `#0b1200` | Text on accent |", "| `--accent-ink` | `#021008` | Text on accent |")
text = text.replace(
    "No purple, no cyan glow, no cream/beige, no gradient text, no chromatic shadows.",
    "No purple, no cyan glow, no cream/beige, no gradient text, no chromatic shadows, no decorative radial washes. The only global texture is the portfolio-family one-axis scanline field.",
)
design.write_text(text)
