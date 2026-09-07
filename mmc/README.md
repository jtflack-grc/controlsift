# MMC / DeepMind weekly deliverables

Handbook track: **Google DeepMind: AI Research Foundations** (GCLP / MMC).

Official labs (vendored): [`vendor/ai-foundations/`](../vendor/ai-foundations/)  
Week ↔ lab map: [`GDM_LAB_MAP.md`](GDM_LAB_MAP.md)  
Show-work notebooks: [`notebooks/`](notebooks/)

| Week | Deliverable | Official GDM (primary) | Our package |
|------|-------------|------------------------|-------------|
| 1 | N-gram + perplexity | `course_1` lab 1_2 | `labs/week01_ngram.py` · `notebooks/week01_ngram.ipynb` |
| 2 | BPE + Data Card | `course_2` lab 2_4 | `week02_bpe` |
| 3 | Skill Badge | Skills / `course_1` 1_5 | `deliverables/week03_skill_badge.md` |
| 4 | MLP from scratch | `course_3` lab 3_4 | `week04_mlp` |
| 5 | Diagnostics | `course_3` 3_5 / 3_6 | `week05_diagnostics` |
| 6 | Attention / decoder | `course_4` 4_1 | `week06_transformer` |
| 7 | LoRA adapter | `course_5` 5_5 / 5_6 | `week07_lora_scaffold` + Gemma path |
| 8 | Alignment & Safety | Course 6 (Skills only) | `week08_alignment_safety_report.md` |
| 9 | Accelerate / memory | `course_7` 7_4–7_6 | `week09_accelerate.md` · notebook |
| 10 | Research proposal | `course_8` prep | `week10_research_proposal.md` |
| 11 | Train / compare | `course_8` classification | `week11_comparative` |
| 12 | Synthesis & defense | Capstone package | `week12_synthesis_defense.md` |

Public hub: [`docs/capstone/deliverables/`](../docs/capstone/deliverables/)

```bash
pip install -e ".[dev]"
python -m mmc.labs.run_all
jupyter notebook mmc/notebooks/week01_ngram.ipynb
pytest tests/test_mmc_labs.py -q
```
