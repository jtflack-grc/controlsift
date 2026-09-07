# One-click ControlSift capstone video record pack (Windows).
# Opens speech-friendly slides + read-aloud script, then reminds Win+G.
# Does NOT start recording — press Win+G yourself after windows load.

$ErrorActionPreference = 'Stop'
$slides = 'https://jtflack-grc.github.io/controlsift/capstone/slides.html?record=1'
$script = 'https://jtflack-grc.github.io/controlsift/capstone/video-script.html'
$saveAs = Join-Path $env:USERPROFILE 'Videos\ControlSift_Capstone_Video.mp4'

Write-Host ''
Write-Host 'ControlSift video pack'
Write-Host '----------------------'
Write-Host "1) Slides (record mode): $slides"
Write-Host "2) Script (read aloud):  $script"
Write-Host "3) Press Win+G → Capture → Start recording"
Write-Host "4) Save/export as:       $saveAs"
Write-Host '5) Upload MP4 to GCLP form only — do NOT git add'
Write-Host ''

Start-Process $slides
Start-Sleep -Milliseconds 600
Start-Process $script

Add-Type -AssemblyName System.Windows.Forms
[void][System.Windows.Forms.MessageBox]::Show(
  "Slides + script opened.`n`nNext:`n• Put slides full-screen (F11)`n• Press Win+G and start capture`n• Read the script aloud (≤5:00)`n• Save as ControlSift_Capstone_Video.mp4`n• Upload to the form — do not commit the MP4",
  'ControlSift — start recording',
  'OK',
  'Information'
)
