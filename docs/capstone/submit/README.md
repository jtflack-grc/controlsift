# Capstone submit exports

Machine-exported PDFs for GCLP form upload (print styles hide nav/footer).

| File | Source |
|------|--------|
| `ControlSift_Capstone_Report.pdf` | `../report.html` |
| `ControlSift_Capstone_Slides.pdf` | `../slides.html` |

Prerequisites:

1. Microsoft Edge (headless PDF)
2. Docs server: `cd docs; python -m http.server 5500`
3. Sources: `../report.html` and `../slides.html`
4. Prefer after full TEST metrics + `after_kaggle` so PDFs show real Gemma F1

```powershell
powershell -File scripts/export_submit_pdfs.ps1
```

**Not included yet:** ≤5-minute video recording (see `../video-script.html` — after-metrics results beat uses placeholders until TEST macro F1 lands).
