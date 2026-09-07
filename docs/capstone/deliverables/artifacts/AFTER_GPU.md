# After smoke / full GPU run — local merge

## Smoke success signals (on Kaggle/Colab)

- `CUDA available: True` and a GPU name
- `transformers` version prints as ≥ 4.50
- `HF login OK; token length = …`
- Baseline / train cells finish without `SystemExit`
- Output includes `controlsift_gpu_outputs.zip`

Smoke writes **validation** metrics only. Do **not** treat those as public Results.

## Full run (required for Pages metrics)

1. Set `SMOKE = False` in the runner config cell
2. Run All again (uses weekly quota)
3. Download `controlsift_gpu_outputs.zip`

## On this PC

```powershell
cd C:\Users\admin\Desktop\sifter
powershell -File scripts/ingest_gpu_outputs.ps1
# or explicitly:
# python scripts/after_kaggle.py --zip "$env:USERPROFILE\Downloads\controlsift_gpu_outputs.zip"
powershell -File scripts/export_submit_pdfs.ps1
```

Then ask the agent to commit + `scripts/push_pages.ps1` when you are ready to publish.
