# After GPU run — local merge

Use this after downloading `controlsift_gpu_outputs.zip` from Kaggle or Colab.

## On this PC

```powershell
cd <repo-root>
python scripts/after_kaggle.py --zip "$env:USERPROFILE\Downloads\controlsift_gpu_outputs.zip"
powershell -File scripts/export_submit_pdfs.ps1
```

## Confirm before publishing

- `results/gemma_*/metrics_test.json` have non-null `macro_f1`
- `docs/data/results.json` matches those TEST values
- Smoke validation (`n=16`) is **not** final — publish only full-run TEST metrics

Public site mirror: `docs/data/results.json` (served under Pages from `docs/`).
