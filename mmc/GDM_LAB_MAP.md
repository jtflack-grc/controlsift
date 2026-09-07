# MMC handbook weeks → DeepMind AI Research Foundations labs

Source of truth for official notebooks: [`vendor/ai-foundations/`](../vendor/ai-foundations/)  
([google-deepmind/ai-foundations](https://github.com/google-deepmind/ai-foundations)).

Course 6 (**Align Your Model**) is on Google Skills but **not** in the public GitHub tree yet.

| Handbook week | Deliverable (checkbox) | Official GDM lab(s) | ControlSift / MMC package |
|---------------|------------------------|---------------------|---------------------------|
| 1 | N-gram generator + perplexity | `course_1/gdm_lab_1_2_experiment_with_n_gram_models.ipynb` (+ compare in `1_3`) | `mmc/notebooks/week01_ngram.ipynb` → `week01_*.json/txt` |
| 2 | Custom BPE + vocab + Data Card | `course_2/gdm_lab_2_4_implement_a_bpe_tokenizer.ipynb` (+ `2_3`) | `week02_bpe.ipynb` + Data Card |
| 3 | DeepMind Skill Badge | Skills path / `course_1` SLM train (`1_5`) | `week03_skill_badge.md` (attach badge) |
| 4 | MLP from scratch | `course_3/gdm_lab_3_4_design_your_own_mlp.ipynb` | `week04_mlp.ipynb` |
| 5 | Diagnostics dashboard | `course_3/gdm_lab_3_5_tune_hyperparameters.ipynb`, `3_6_mitigate_overfitting.ipynb` | `week05_diagnostics.ipynb` + HTML dashboard |
| 6 | Transformer + attention viz | `course_4/gdm_lab_4_1_attention_visualization.ipynb` (+ `4_2`/`4_3`) | `week06_transformer.ipynb` |
| 7 | Domain adapter checkpoint | `course_5/gdm_lab_5_5_implement_lora…`, `5_6_fine_tune_gemma_with_lora.ipynb` | `week07_lora.ipynb` + Gemma QLoRA path |
| 8 | Alignment & Safety Report | Course 6 (Skills; labs not public) | `week08_alignment_safety_report.md` + Assurance |
| 9 | Accelerate / memory profile | `course_7/gdm_lab_7_4_estimate_gpu_memory.ipynb` (+ `7_5`, `7_6`) | `week09_accelerate.md` + notes notebook |
| 10 | Research proposal + baselines | `course_8` classification prep (`8_1`–`8_2`) | `week10_*.md` + classical Results |
| 11 | Weights / logs / comparative | `course_8` classification train/eval (`8_3`) | `week11_*.ipynb` + comparative JSON |
| 12 | Synthesis & defense | Capstone package (`course_8` track) | report / slides / video / paper |

## Exceed bar (ControlSift)

Official labs teach the technique. We exceed the checkbox when we also ship:

1. Frozen ControlSift research surface (synthetic evidence quality, 5-class)
2. Machine-readable artifacts under `mmc/deliverables/outputs/`
3. Public docs hub with direct links (no fabricated Gemma metrics)
4. Assurance / Data Card / RAI wiring where the week calls for it
