# Export report + slides to PDF for GCLP form upload.
# Requires: local docs server on http://127.0.0.1:5500 and Microsoft Edge.

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$OutDir = Join-Path $Root "docs\capstone\submit"
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
