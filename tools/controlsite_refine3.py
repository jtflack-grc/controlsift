from pathlib import Path

path = Path("docs/assets/css/site.css")
css = path.read_text()
css = css.replace("font-size: 0.72rem;\n  letter-spacing: 0.02em;\n  color: #38e881 !important;", "font-size: var(--text-xs);\n  letter-spacing: 0.02em;\n  color: #38e881 !important;", 1)
css = css.replace("font-size: var(--text-xs);\n  color: var(--accent-2);\n  letter-spacing: 0.03em;\n  animation: rise 1s ease 0.2s forwards;", "font-size: var(--text-sm);\n  color: var(--accent-2);\n  letter-spacing: 0.015em;\n  animation: rise 1s ease 0.2s forwards;", 1)
css = css.replace("letter-spacing: 0.05em;\n  text-transform: uppercase;\n}\n\n.def-list dd", "letter-spacing: 0.015em;\n  text-transform: none;\n}\n\n.def-list dd", 1)
css = css.replace("letter-spacing: 0.04em;\n  text-transform: uppercase;\n  margin-bottom: 0.65rem;", "letter-spacing: 0.015em;\n  text-transform: none;\n  margin-bottom: 0.65rem;", 1)
path.write_text(css)
