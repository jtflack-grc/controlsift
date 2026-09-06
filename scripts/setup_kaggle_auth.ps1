# One-time Kaggle API auth (optional — Dataset UI upload works without this)

# 1) Open https://www.kaggle.com/settings → API → Create New Token
# 2) Move the downloaded kaggle.json here (never commit it; gitignored):

$DestDir = Join-Path $env:USERPROFILE ".kaggle"
New-Item -ItemType Directory -Force -Path $DestDir | Out-Null
$Src = Join-Path $env:USERPROFILE "Downloads\kaggle.json"
if (-not (Test-Path $Src)) {
  Write-Host "Download kaggle.json from Kaggle Settings → API, then re-run this script."
  Start-Process "https://www.kaggle.com/settings"
  exit 1
}
Copy-Item -Force $Src (Join-Path $DestDir "kaggle.json")
icacls (Join-Path $DestDir "kaggle.json") /inheritance:r /grant:r "$env:USERNAME:(R)" | Out-Null
Write-Host "Installed $DestDir\kaggle.json"
Write-Host "Optional CLI upload after editing dist/kaggle_dataset/dataset-metadata.yaml id:"
Write-Host "  pip install kaggle"
Write-Host "  kaggle datasets create -p dist/kaggle_dataset --dir-mode zip"
