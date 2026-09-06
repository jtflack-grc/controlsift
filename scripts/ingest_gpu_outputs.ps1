# Find controlsift_gpu_outputs.zip (Downloads or Desktop) and merge into the repo.
# Usage: powershell -File scripts/ingest_gpu_outputs.ps1

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

$candidates = @(
  (Join-Path $env:USERPROFILE "Downloads\controlsift_gpu_outputs.zip"),
  (Join-Path $env:USERPROFILE "Desktop\controlsift_gpu_outputs.zip"),
  (Join-Path $Root "controlsift_gpu_outputs.zip"),
  (Join-Path $Root "dist\controlsift_gpu_outputs.zip")
)

$zip = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $zip) {
  $found = Get-ChildItem (Join-Path $env:USERPROFILE "Downloads"), (Join-Path $env:USERPROFILE "Desktop") -Filter "*gpu*output*.zip" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
  if ($found) { $zip = $found.FullName }
}

if (-not $zip) {
  Write-Host "No controlsift_gpu_outputs.zip found in Downloads/Desktop/repo."
  Write-Host "Download it from the Kaggle Output panel after the package cell finishes."
  exit 1
}

Write-Host "Using $zip"
python scripts/after_kaggle.py --zip $zip
Write-Host "Next: set SMOKE=False on Kaggle for public test metrics if this was smoke-only."
Write-Host "Then: powershell -File scripts/export_submit_pdfs.ps1"
