# DESIGN.md - ControlSift

## Visual system
Portfolio-family research surface. Near-black green canvas with the same restrained horizontal phosphor scanline field as the main portfolio. Clinical, forensic, receipt-driven - not SaaS launch energy.

## Colors
| Token | Value | Use |
|-------|-------|-----|
| `--bg` | `#050a08` | Portfolio-aligned near-black canvas |
| `--fg` | `#e8f4ec` | Primary text |
| `--muted` | `#91aa9b` | Secondary text |
| `--line` | `rgba(105, 255, 164, 0.16)` | Hairlines |
| `--panel` | `#09110d` | Recessed panels |
| `--accent` | `#7fffb2` | Signal / primary actions |
| `--accent-ink` | `#021008` | Text on accent |
| `--warn` | `#f0a35a` | Caution / insufficient |
| `--danger` | `#ff7a7a` | Contradictory / error |

No purple, no cyan glow, no cream/beige, no gradient text, no chromatic shadows, no decorative radial washes. The only global texture is the portfolio-family one-axis scanline field.

## Typography
| Role | Family |
|------|--------|
| Display / brand | IBM Plex Sans |
| Body / UI | IBM Plex Sans |
| Metrics / tags / code | IBM Plex Mono |

Portfolio-aligned: IBM Plex only (no serif display faces).

Ramp: 12 / 17 / 28 / 44 / 72 (px). Prefer large jumps over many close sizes.

## Shape
Radius **2px** maximum. No pills (`999px`). No soft multi-layer “AI glow” washes.

## Components
- Nav: sticky, hairline bottom, transparent on black
- Buttons: flat fill or hairline outline, sharp
- Evidence compare: split panes with hairline, not stacked marketing cards
- Metrics: mono numerals, minimal chrome
- Tables: hairline grid on black

## Motion
Opacity/transform fade only, short, `ease`. No bounce/elastic. Respect `prefers-reduced-motion`.
