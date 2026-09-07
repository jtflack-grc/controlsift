# After smoke / full GPU run — local merge

## Smoke success signals (on Kaggle/Colab)

- `CUDA available: True` and a GPU name
- `transformers` version prints as ≥ 4.50
- `HF login OK; token length = …`
- Train prints `TrainingArguments keys: […]` then finishes without `SystemExit`
- Output includes `controlsift_gpu_outputs.zip`

If train fails with `unexpected keyword argument 'warmup_ratio'`, re-run the
**Locate or fetch repo** cell (fresh clone of `kaggle-bundle`), then install → train again.

Smoke writes **validation** metrics only. Do **not** treat those as public Results.

## FULL RUN (required for public / Pages metrics)

Smoke validation (`n=16`) is **not** final. Do **not** publish smoke F1 as Results.

1. In Config cell set **`SMOKE = False`** (keep `SMOKE_LIMIT` unused for full).
2. **Run All** again — expect **much longer** runtime (full val + test + challenge; train if needed). Weekly GPU quota applies.
3. When Output shows `controlsift_gpu_outputs.zip`, **download** it to Downloads (overwrite the smoke zip is OK).
4. On this PC, merge with after_kaggle (watcher may auto-trigger):

```powershell
cd C:\Users\admin\Desktop\sifter
python scripts/after_kaggle.py --zip "$env:USERPROFILE\Downloads\controlsift_gpu_outputs.zip"
# or: powershell -File scripts/ingest_gpu_outputs.ps1
powershell -File scripts/export_submit_pdfs.ps1
```

Confirm `results/gemma_*/metrics_test.json` have non-null `macro_f1` before any Pages publish.
Then ask the agent to commit + `scripts/push_pages.ps1` when you are ready.
