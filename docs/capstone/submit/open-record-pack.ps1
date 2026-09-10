# One-click ControlSift capstone recording helper for Windows.
# Opens the final deck page and browser teleprompter.
# It does not start recording automatically.

$ErrorActionPreference = 'Stop'
$deck = 'https://jtflack-grc.github.io/controlsift/capstone/slides.html'
$teleprompter = 'https://jtflack-grc.github.io/controlsift/capstone/video-script.html?teleprompter=1'
$saveAs = Join-Path $env:USERPROFILE 'Videos\ControlSift_Capstone_Video.mp4'

Write-Host ''
Write-Host 'ControlSift final video pack'
Write-Host '---------------------------'
Write-Host "1) Final PowerPoint deck: $deck"
Write-Host "2) Browser teleprompter:  $teleprompter"
Write-Host '3) PowerPoint Record > From Beginning, or use your screen recorder'
Write-Host '4) Hard cap: 5:00; script target is about 4:50'
Write-Host "5) Save/export as:        $saveAs"
Write-Host '6) Upload the MP4 to the capstone form only; do not commit it'
Write-Host ''

Start-Process $deck
Start-Sleep -Milliseconds 600
Start-Process $teleprompter

Add-Type -AssemblyName System.Windows.Forms
[void][System.Windows.Forms.MessageBox]::Show(
  "Final deck + teleprompter opened.`n`nThe PPTX on the deck page contains the full narration in speaker notes.`n`nTarget: about 4:50. Hard cap: 5:00.`nSave as ControlSift_Capstone_Video.mp4 and upload it to the form only.",
  'ControlSift - final recording',
  'OK',
  'Information'
)
