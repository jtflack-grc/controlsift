# ControlSift final capstone submission pack

The ControlSift capstone artifact is complete: final report, eight-slide PowerPoint deck, narrated presentation, public research site, and supporting research/governance evidence.

## Form-ready artifacts

| Field / artifact | Value / path | Status |
|---|---|---|
| GitHub Pages site | https://jtflack-grc.github.io/controlsift/ | Complete |
| Capstone report PDF | `ControlSift_Capstone_Report.pdf` | Complete |
| PowerPoint deck | `ControlSift_Capstone_Slides.pptx` | Complete |
| Slides PDF | `ControlSift_Capstone_Slides.pdf` | Complete |
| Final narrated presentation | https://github.com/jtflack-grc/controlsift/releases/download/v1.0-capstone/ControlSift_Capstone_Slides.mp4 | Complete |
| Final release | https://github.com/jtflack-grc/controlsift/releases/tag/v1.0-capstone | Complete |
| Week-3 skill badge | https://www.skills.google/public_profiles/a6a2045d-a94e-4ea5-a1f1-7752f2dab561/badges/26439446 | Complete |

The video is stored as a GitHub Release asset rather than committed into repository history. The release is tagged `v1.0-capstone`.

## Research-integrity boundary

Classical results are from dataset v1.1.0; completed Gemma results are from v1.0.0. The project publishes both sets of scores but does not claim a controlled cross-version leaderboard.

## PowerPoint generation

The eight-slide deck is generated from:

`../../../scripts/build_capstone_deck.js`

GitHub Actions can rebuild the PPTX and PDF when the deck source changes. The generated presentation uses ordinary Office-safe fonts and embeds the final narration as PowerPoint speaker notes.

## Program submission

When the MMC submission portal calls for the final package, use the artifacts above. That portal upload is administrative; the ControlSift project and rubric-facing deliverables are complete.
