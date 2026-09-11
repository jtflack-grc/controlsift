# DESIGN.md - ControlSift

## Visual system
OLED-first research surface. True black canvas for emissive displays. Clinical, forensic, receipt-driven - not SaaS launch energy.

## Colors
| Token | Value | Use |
|-------|-------|-----|
| `--bg` | `#000000` | Page canvas (OLED intentional) |
| `--fg` | `#e7e9e4` | Primary text |
| `--muted` | `#9aa39a` | Secondary text |
| `--line` | `#1a1d1a` | Hairlines |
| `--panel` | `#070807` | Recessed panels (near-black, not gray card) |
| `--accent` | `#d2f27a` | Signal / primary actions |
| `--accent-ink` | `#0b1200` | Text on accent |
| `--warn` | `#f0a35a` | Caution / insufficient |
| `--danger` | `#ff7a7a` | Contradictory / error |

No purple, no cyan glow, no cream/beige, no gradient text, no chromatic shadows.

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
