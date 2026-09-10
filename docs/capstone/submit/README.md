# ControlSift final capstone submission pack

Final report, actual PowerPoint deck, teleprompter, and form-ready links for the MMC / Google Cloud Launchpad capstone. **Do not commit the video file.**

## Form-ready artifacts

| Field / artifact | Value / path | Status |
|---|---|---|
| GitHub Pages site | https://jtflack-grc.github.io/controlsift/ | Ready |
| Capstone report PDF | `ControlSift_Capstone_Report.pdf` | Ready |
| PowerPoint deck | `ControlSift_Capstone_Slides.pptx` | Ready |
| Slides PDF | `ControlSift_Capstone_Slides.pdf` | Ready |
| Final teleprompter | `ControlSift_Video_Teleprompter.txt` | Ready |
| Browser teleprompter | [../video-script.html](../video-script.html) | Ready |
| Week-3 skill badge | https://www.skills.google/public_profiles/a6a2045d-a94e-4ea5-a1f1-7752f2dab561/badges/26439446 | Ready |
| Final video | `ControlSift_Capstone_Video.mp4` | **Record and submit** |

## Recording path

The PowerPoint is the canonical presentation artifact. It contains the exact final narration in the speaker notes.

1. Open `ControlSift_Capstone_Slides.pptx` in PowerPoint.
2. Use **Record > From Beginning** for a native narrated deck, or present full-screen and capture it with your preferred screen recorder.
3. Read the speaker notes word-for-word. The narration is about 700 spoken words and is timed for roughly **4:50 at 145 words per minute**.
4. A larger browser teleprompter is available at `../video-script.html?teleprompter=1`. Controls: Space/Page Down/Arrow Down = next block; Page Up/Arrow Up = previous; `T` = timer start/pause; `R` = reset.
5. Keep the final recording at or below the rubric's **5:00 hard cap**.
6. Save the MP4 locally and upload it through the program form. Do not add the MP4 to git.

The narration deliberately states the research-integrity boundary: classical results are from dataset v1.1.0; completed Gemma results are from v1.0.0. It does not claim a controlled cross-version leaderboard.

## PowerPoint generation

The eight-slide deck is generated from:

`../../../scripts/build_capstone_deck.js`

GitHub Actions rebuilds the PPTX and PDF when the deck source or final script changes. The generated presentation uses ordinary Office-safe fonts and embeds the narration as PowerPoint speaker notes.

## What remains

- [ ] Record `ControlSift_Capstone_Video.mp4` at <=5:00.
- [ ] Upload the report, slides, site/badge links, and video through the capstone form.

Everything else in the capstone research package is complete.
