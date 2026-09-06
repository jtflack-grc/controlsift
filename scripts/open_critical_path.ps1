# Opens the critical-path surfaces for the next Kaggle / badge / submit session.
# Does not touch secrets.

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Zip = Join-Path $Root "dist\controlsift_kaggle_bundle.zip"
$urls = @(
  "http://127.0.0.1:5500/capstone/next-steps.html",
  "http://127.0.0.1:5500/capstone/kaggle-checklist.html",
  "http://127.0.0.1:5500/capstone/deliverables/artifacts/KAGGLE_SAFE_RUN.md.html",
  "http://127.0.0.1:5500/capstone/submit/",
  "https://huggingface.co/google/gemma-3-1b-it",
  "https://huggingface.co/settings/tokens",
  "https://www.kaggle.com/datasets?new=true"
)
foreach ($u in $urls) {
  try { Start-Process $u } catch { Write-Host "Could not open $u" }
}
Start-Process explorer.exe "/select,$Zip"
Write-Host "Opened critical-path pages + selected Kaggle zip."
Write-Host "Ladder: HF license → Read token → upload zip as private Dataset → Notebook GPU + HF_TOKEN secret → SMOKE=True → SMOKE=False → download outputs →"
Write-Host '  python scripts/after_kaggle.py --zip "$env:USERPROFILE\Downloads\controlsift_gpu_outputs.zip"'
