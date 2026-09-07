# Week 12 deliverable — Synthesis & Defense

**Handbook:** Course 08 · Capstone – Synthesis & Defense  
**Milestone 4:** Final Capstone AI Research Paper, GitHub repo, and defense

## 1. Research paper (4–6 pages)

Handbook asks for a **4–6 page** AI research paper. Use:

| Artifact | Role |
|----------|------|
| `docs/capstone/report.html` | Printable submission-length report (stay within ~4–6 pages when printed compactly / trim to 6 if needed) |
| `docs/capstone/paper.html` | Long-form narrative for deep review (not the length-limited upload) |

Print `report.html` → PDF for form upload.

## 2. Open-source / documented GitHub repository

| Requirement | Location |
|-------------|----------|
| Documented README | `README.md` (CRISP-DM + results) |
| Repro instructions | `docs/reproduce.html` · README |
| Code | `src/controlsift/` · `mmc/labs/` · `scripts/` |
| Data docs | `data/README.md` · Data Card |
| Reflection | `reflection/project_reflection.md` |

## 3. Final presentation / defense

| Piece | Artifact | Status |
|-------|----------|--------|
| ≤8 slides | `docs/capstone/slides.html` | ready |
| ≤5 min talk track | `docs/capstone/video-script.html` | script ready |
| Recorded video | scholar recording | **pending** |
| Defense Q&A notes | section 5 below | ready |

## 4. Defense packet (anticipated questions)

1. **Why synthetic data?** Privacy + leakage control; disclosed compositional surface.  
2. **Why SDG 10 not 16?** GCLP requires one of Goals 1/2/3/10/13; inequality of assurance access is the official selection.  
3. **Did PEFT help?** Answer only after Gemma result files exist — currently null.  
4. **Is this an auditor?** No. Intended Use forbids production audit replacement.  
5. **Why TF-IDF isn’t “solved”?** Early leakage fixed in v1.1; ceiling ~0.53.  
6. **What would you do with more time?** Real GRC spot-check; LLM Failure Lab; optional larger model.

## 5. Status

| Item | Status |
|------|--------|
| Paper / report | ready |
| GitHub documentation | ready |
| Slides + script | ready |
| Video / live defense | pending scholar |
| LLM results in paper | pending GPU |

`partial` until video + Gemma numbers land.
