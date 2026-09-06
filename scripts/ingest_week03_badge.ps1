# One-shot: copy a badge screenshot/PDF into the Week 3 drop zone and sync the hub.
# Usage:
#   powershell -File scripts/ingest_week03_badge.ps1 -Source "C:\Users\admin\Downloads\my-badge.png"
# Optional:
#   -CredentialUrl "https://..." -EarnedDate "2026-08-15"

param(
  [Parameter(Mandatory = $true)][string]$Source,
  [string]$CredentialUrl = "",
  [string]$EarnedDate = ""
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Src = Resolve-Path $Source
$Ext = [IO.Path]::GetExtension($Src).ToLowerInvariant()
if ($Ext -notin @(".png", ".jpg", ".jpeg", ".pdf", ".webp")) {
  throw "Expected png/jpg/pdf/webp, got $Ext"
}
if ($Ext -eq ".jpeg") { $Ext = ".jpg" }
if ($Ext -eq ".webp") { $Ext = ".png" }

$OutDir = Join-Path $Root "mmc\deliverables\outputs"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$Dest = Join-Path $OutDir ("week03_skill_badge" + $Ext)
Copy-Item -Force $Src $Dest
Write-Host "Copied -> $Dest"

$Md = Join-Path $Root "mmc\deliverables\week03_skill_badge.md"
$text = Get-Content -Raw -Path $Md
$text = $text -replace '`awaiting_proof_file`', '`proof_attached`'
if ($EarnedDate) {
  $text = $text -replace '\| Earned date \| _TBD[^\|]*\|', "| Earned date | $EarnedDate |"
}
if ($CredentialUrl) {
  $text = $text -replace '\| Credential URL \| _TBD[^\|]*\|', "| Credential URL | $CredentialUrl |"
}
$text = $text -replace '\| Local proof file \| `[^`]+` \|', "| Local proof file | ``mmc/deliverables/outputs/week03_skill_badge$Ext`` |"
Set-Content -Path $Md -Value $text -Encoding utf8
Write-Host "Updated $Md"

Set-Location $Root
python -m mmc.labs.sync_artifacts | Out-Null
python -m mmc.labs.build_week_pages | Out-Null
Write-Host "Synced deliverables hub. Open: http://127.0.0.1:5500/capstone/deliverables/week03.html"
