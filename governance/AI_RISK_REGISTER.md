# AI Risk Register - ControlSift

| ID | Risk | Likelihood | Impact | Mitigation | Status |
|----|------|------------|--------|------------|--------|
| R1 | Users treat model as automated auditor | Medium | High | Explicit non-claims on site, README, Model Card | Open |
| R2 | Synthetic-to-real generalization overstated | High | High | Challenge set, Failure Lab, limitations docs | Open |
| R3 | Label leakage / family leakage invalidates results | Medium | High | Family splits, CI leakage tests, protocol seal | Mitigated |
| R4 | Lexical shortcuts inflate apparent difficulty reduction | Medium | Medium | TF-IDF Gate 1 check; harden mutations | Mitigated |
| R5 | Prompt tuning on test set | Low | High | Protocol lock; AGENTS.md rules | Mitigated |
| R6 | Fabricated or placeholder metrics published | Low | High | Null-until-run results policy; CI integrity | Mitigated |
| R7 | Secret / credential exposure in notebooks | Medium | High | .gitignore; SECURITY.md; no tokens in repo | Mitigated |
| R8 | Overclaiming from tiny F1 deltas | Medium | Medium | Bootstrap CIs; cautious reporting language | Open |
| R9 | MMC rubric changes distract from research quality | Low | Low | Modular `/capstone/` page | Accepted |
| R10 | Free GPU unavailable delays Gemma runs | Medium | Medium | Kaggle primary, Colab fallback, 1B model | Open |
