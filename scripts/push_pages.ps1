# Push ControlSift to GitHub Pages after you approve a commit.
# Does NOT commit for you. Does NOT push secrets.
#
# Prerequisites:
#   1) Gemma metrics in results/gemma_*/metrics_test.json (or intentional nulls)
#   2) You have reviewed `git status` and staged a clean commit yourself
#   3) origin = https://github.com/jtflack-grc/controlsift.git
#
# Usage (after your commit exists on the current branch):
#   powershell -File scripts/push_pages.ps1

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

$remote = git remote get-url origin 2>$null
if (-not $remote) { throw "No origin remote. Expected jtflack-grc/controlsift." }

$status = git status --porcelain
if ($status) {
  Write-Host "Working tree has uncommitted changes. Commit first (agent will not auto-commit)."
  Write-Host $status
  exit 1
}

$branch = (git rev-parse --abbrev-ref HEAD).Trim()
Write-Host "Pushing $branch → origin (remote default is main)..."

# Prefer pushing local branch to remote main for Pages workflow.
if ($branch -eq "master") {
  git push -u origin master:main
} else {
  git push -u origin HEAD
}

Write-Host "Next: GitHub → Settings → Pages → Source = GitHub Actions (if not already)."
Write-Host "Site: https://jtflack-grc.github.io/controlsift/"
