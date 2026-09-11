# Week 12 deliverable - Synthesis & Defense

**Handbook:** Course 08 · Capstone – Synthesis & Defense  
**Milestone 4:** Final Capstone AI Research Paper, GitHub repo, and defense

## 1. Research paper

| Artifact | Role | Status |
|----------|------|--------|
| `docs/capstone/submit/ControlSift_Capstone_Report.pdf` | Rubric-facing final report | complete |
| `docs/capstone/paper.html` | Long-form technical narrative | complete |

## 2. Open-source / documented GitHub repository

| Requirement | Location |
|-------------|----------|
| Documented README | `README.md` - problem, method, results, limits, CRISP-DM |
| Repro instructions | `docs/reproduce.html` · README |
| Code | `src/controlsift/` · `mmc/labs/` · `scripts/` |
| Data docs | `data/README.md` · Data Card |
| Reflection | `reflection/project_reflection.md` |
| Final release | `v1.0-capstone` |

## 3. Final presentation / defense

| Piece | Artifact | Status |
|-------|----------|--------|
| ≤8 slides | `docs/capstone/submit/ControlSift_Capstone_Slides.pptx` | complete |
| Slides PDF | `docs/capstone/submit/ControlSift_Capstone_Slides.pdf` | complete |
| ≤5 min narrated presentation | `https://github.com/jtflack-grc/controlsift/releases/download/v1.0-capstone/ControlSift_Capstone_Slides.mp4` | complete |
| Defense Q&A notes | section 4 below | complete |

## 4. Defense packet

1. **Why synthetic data?** Privacy, repeatability, and leakage control. The synthetic-to-real limitation is explicitly disclosed.  
2. **Why Reduced Inequalities?** MMC rubric option 4 is Reduced Inequalities; the official UN designation is SDG 10. The project frames assurance access as a resource constraint, not as proof that AI should replace staff.  
3. **Did PEFT help?** Within the controlled Gemma v1.0 experiments, no. Few-shot macro F1 was about 0.137; QLoRA was about 0.083 and had poor parse reliability.  
4. **Did TF-IDF beat Gemma?** The published values suggest a large difference, but they're from different dataset versions. Classical experiments use v1.1.0 and Gemma uses v1.0.0, so ControlSift doesn't claim a controlled cross-family win.  
5. **Is this an auditor?** No. Intended Use explicitly forbids production audit replacement or autonomous compliance conclusions.  
6. **What was the most important research lesson?** A benchmark must earn its difficulty, fine-tuning doesn't guarantee improvement, and an honest negative result is more useful than manufacturing an AI success story.

## 5. Completion status

| Item | Status |
|------|--------|
| Paper / report | complete |
| GitHub documentation | complete |
| Slides | complete |
| Narrated presentation | complete |
| Gemma results | complete / v1.0.0 |
| Classical results | complete / v1.1.0 |
| Failure analysis + assurance package | complete |

All rubric-facing ControlSift artifacts are complete. Any later MMC portal upload is administrative only.
