# Export report + slides to PDF for GCLP form upload.
#
# Prerequisites (all required before run):
#   1) Microsoft Edge installed (headless --print-to-pdf)
#   2) Docs HTTP server:  cd docs; python -m http.server 5500
#   3) Sources exist:
#        docs/capstone/report.html  -> ControlSift_Capstone_Report.pdf
#        docs/capstone/slides.html  -> ControlSift_Capstone_Slides.pdf
#   4) Prefer running AFTER full TEST metrics + after_kaggle (so PDFs show real Gemma F1)
#
# Usage (repo root):
#   powershell -File scripts/export_submit_pdfs.ps1

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$OutDir = Join-Path $Root "docs\capstone\submit"
$ReportHtml = Join-Path $Root "docs\capstone\report.html"
$SlidesHtml = Join-Path $Root "docs\capstone\slides.html"
if (-not (Test-Path $ReportHtml)) { throw "Missing source: docs/capstone/report.html" }
if (-not (Test-Path $SlidesHtml)) { throw "Missing source: docs/capstone/slides.html" }

$Edge = @(
  "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
  "${env:ProgramFiles}\Microsoft\Edge\Application\msedge.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $Edge) { throw "Microsoft Edge not found (needed for headless PDF)." }

try {
  $null = Invoke-WebRequest -Uri "http://127.0.0.1:5500/capstone/report.html" -UseBasicParsing -TimeoutSec 3
} catch {
  throw "Start the docs server first: cd docs; python -m http.server 5500"
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$jobs = @(
  @{ Url = "http://127.0.0.1:5500/capstone/report.html"; Out = Join-Path $OutDir "ControlSift_Capstone_Report.pdf" },
  @{ Url = "http://127.0.0.1:5500/capstone/slides.html"; Out = Join-Path $OutDir "ControlSift_Capstone_Slides.pdf" }
)

foreach ($j in $jobs) {
  if (Test-Path $j.Out) { Remove-Item $j.Out -Force }
  Write-Host "Printing $($j.Url) -> $($j.Out)"
  & $Edge --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="$($j.Out)" $j.Url | Out-Null
  $deadline = (Get-Date).AddSeconds(20)
  while (-not (Test-Path $j.Out) -and (Get-Date) -lt $deadline) { Start-Sleep -Milliseconds 400 }
  if (-not (Test-Path $j.Out)) { throw "PDF not written: $($j.Out)" }
  Write-Host "OK $((Get-Item $j.Out).Length) bytes"
}

Write-Host "Submit PDFs ready in $OutDir"
