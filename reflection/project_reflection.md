# Project reflection - ControlSift

Brief reflection for the GCLP Capstone GitHub structure requirement.

## What I learned

- Sealing evaluation before model claims keeps the research honest.
- Lexical baselines can “solve” a bad dataset; hardening the data restored a real research question.
- Fine-tuning doesn't automatically improve a small model: within the completed Gemma v1.0 experiments, few-shot prompting outperformed QLoRA.
- Output-contract reliability belongs in model evaluation. QLoRA test parse success of about 0.435 was a substantive failure mode, not a formatting nuisance.
- Responsible AI artifacts (Data Card, Model Card, Risk Register, Intended Use) are part of the research product, not an appendix.
- Dataset and protocol provenance matter. The final review found that the classical experiments use v1.1 while Gemma uses v1.0, so the project explicitly avoids a false same-benchmark cross-family ranking.

## Challenges faced

- Free-tier GPU constraints limited the practical ability to repeat the entire model ladder after the dataset-version boundary was discovered.
- Balancing MMC’s “Reduced Inequalities” option with the official UN SDG 10 designation and keeping the access-to-assurance argument appropriately bounded.
- Avoiding overclaim: synthetic compositional packets aren't naturalistic evidence binders, and structural/scripted label checks aren't an independent human gold standard.
- Preserving an inconvenient negative result instead of treating fine-tuning itself as evidence of improvement.

## Improvements with more time

These are possible future research directions, not incomplete capstone requirements:

- Run classical and language-model experiments on one common dataset version for a controlled cross-family comparison.
- Improve constrained decoding and label-output reliability before additional model claims.
- Add independent human expert review and, where governance permits, carefully controlled real-world evidence validation.
- Expand slice-level and qualitative error analysis around the hardest evidence boundaries.

## Final status

The ControlSift research artifact and MMC capstone package are complete. Classical results are published on dataset v1.1.0; Gemma zero-shot, few-shot, and QLoRA results are published on dataset v1.0.0; the version boundary is disclosed throughout the final materials; and the report, slides, final narrated presentation, assurance artifacts, and supporting documentation are finished.
