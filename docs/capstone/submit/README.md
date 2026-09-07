# Capstone submit pack (GCLP form upload)

Machine-exported PDFs plus live links for the MMC / GCLP submission form.
Print styles hide nav/footer. **Do not commit** large video files.

## Form upload checklist

Use these exact artifacts when filling the form:

| Field / artifact | Value / path | Status |
|------------------|--------------|--------|
| GitHub Pages site | https://jtflack-grc.github.io/controlsift/ | Live (HTTP 200) |
| Live TEST metrics | https://jtflack-grc.github.io/controlsift/data/results.json | Gemma ladder non-null |
| Capstone report PDF | `ControlSift_Capstone_Report.pdf` (this folder) | Ready |
| Capstone slides PDF | `ControlSift_Capstone_Slides.pdf` (this folder) | Ready |
| Week-3 skill badge URL | https://www.skills.google/public_profiles/a6a2045d-a94e-4ea5-a1f1-7752f2dab561/badges/26439446 | Ready |
| Badge proof (Pages) | https://jtflack-grc.github.io/controlsift/capstone/deliverables/ | Linked on Weekly Labs |
| ≤5-min video | `ControlSift_Capstone_Video.mp4` | **Missing — record next** |
| Video script (read-aloud) | [../video-script.html](../video-script.html) | Metrics filled; ≤5:00 |

### Video recording (remaining) — one-click open

**NOT FOUND on disk yet** (searched Downloads / Desktop / Videos / Documents / sifter for `ControlSift*Video*.mp4` and `*capstone*video*.mp4`). Record next:

1. **One-click open** (from this folder):
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\open-record-pack.ps1
   ```
   That opens:
   - Slides (record mode): https://jtflack-grc.github.io/controlsift/capstone/slides.html?record=1
   - Script: https://jtflack-grc.github.io/controlsift/capstone/video-script.html
2. Press **Win+G** → Capture → Start recording (Xbox Game Bar). Put slides **F11** full-screen.
3. Read the script aloud — speak the published TEST macro F1 values already in the script.
4. Export / save as `%USERPROFILE%\Videos\ControlSift_Capstone_Video.mp4` (≤5:00). Keep it **out of git**; upload to the form only.
5. Confirm spoken numbers match on-screen slides and `docs/data/results.json`.

Offline fallbacks: [slides.html](../slides.html)?record=1 and [video-script.html](../video-script.html) (or the slides PDF above).

## PDF exports in this folder

| File | Source |
|------|--------|
| `ControlSift_Capstone_Report.pdf` | `../report.html` |
| `ControlSift_Capstone_Slides.pdf` | `../slides.html` |

Prerequisites to regenerate:

1. Microsoft Edge (headless PDF)
2. Docs server: `cd docs; python -m http.server 5500`
3. Prefer after TEST metrics are in `docs/data/results.json` (already published)

```powershell
powershell -File scripts/export_submit_pdfs.ps1
```

## Not done yet

- [ ] Record and upload `ControlSift_Capstone_Video.mp4` (form only; do not commit)
- [ ] Submit the GCLP form with Pages + PDFs + badge URL + video
