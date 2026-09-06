# Launch JupyterLab for MMC notebooks from repo root.
# Prefers conda env `controlsift-mmc` if present; else current Python.

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

$Conda = @(
  "$env:USERPROFILE\anaconda3\Scripts\conda.exe",
  "$env:USERPROFILE\miniconda3\Scripts\conda.exe",
  "$env:LOCALAPPDATA\anaconda3\Scripts\conda.exe",
  "$env:LOCALAPPDATA\miniconda3\Scripts\conda.exe",
  "C:\ProgramData\anaconda3\Scripts\conda.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

$EnvName = "controlsift-mmc"
$NotebookDir = Join-Path $Root "mmc\notebooks"
$StartNb = Join-Path $NotebookDir "week01_ngram.ipynb"

function Test-EnvExists {
  param([string]$CondaExe, [string]$Name)
  & $CondaExe env list | Select-String -Pattern "^\s*$Name\s" -Quiet
}

$JupyterExe = Join-Path $env:USERPROFILE "anaconda3\envs\$EnvName\Scripts\jupyter.exe"
if (-not (Test-Path $JupyterExe)) {
  $JupyterExe = Join-Path $env:LOCALAPPDATA "anaconda3\envs\$EnvName\Scripts\jupyter.exe"
}

if ((Test-Path $JupyterExe)) {
  Write-Host "Using conda env: $EnvName"
  Write-Host "JupyterLab → $NotebookDir"
  Write-Host "Open Week 1: $StartNb"
  & $JupyterExe lab --notebook-dir="$Root" "$StartNb"
} elseif ($Conda -and (Test-EnvExists -CondaExe $Conda -Name $EnvName)) {
  Write-Host "Using conda env via conda run: $EnvName"
  & $Conda run -n $EnvName jupyter lab --notebook-dir="$Root" "$StartNb"
} elseif ($Conda) {
  Write-Host "Conda found but env '$EnvName' missing."
  Write-Host "Create it with:"
  Write-Host "  & `"$Conda`" env create -f `"$Root\environment-mmc.yml`""
  Write-Host "Then re-run this script."
  exit 1
} else {
  Write-Host "No conda found — using: $(python -c 'import sys; print(sys.executable)')"
  python -c "import jupyterlab" 2>$null
  if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing notebook extras into current Python..."
    python -m pip install -e ".[dev,notebooks]"
  }
  python -m jupyter lab --notebook-dir="$Root" "$StartNb"
}
