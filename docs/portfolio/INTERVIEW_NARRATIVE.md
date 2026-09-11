# Interview Narrative - ControlSift

## 60 seconds

ControlSift asks whether a small model can tell proof from paperwork in cybersecurity evidence. I built a synthetic, family-isolated benchmark, caught a TF-IDF shortcut that scored 1.0, hardened the classical benchmark to about 0.53 macro F1, locked the evaluation protocol, and ran Gemma 3 zero-shot, few-shot, and QLoRA experiments. The useful result wasn't an AI victory: within the Gemma v1.0 runs, few-shot was strongest and QLoRA didn't improve on it. I also found and disclosed that the completed classical work used dataset v1.1 while the Gemma runs used v1.0, so I don't present those cross-family scores as a controlled same-benchmark comparison.

## Five minutes

Most fine-tuning demos stop at training loss. I treated this as AI assurance: family-isolated splits, TF-IDF as a lexical-shortcut detector, a compositional packet format disclosed so I don't overclaim naturalistic binder judgment, protocol sealing, machine-readable metrics, failure analysis, and explicit human-review boundaries. The first synthetic generator was too easy and let TF-IDF saturate at 1.0, so I hardened the benchmark before the final classical evaluation. The Gemma experiments then produced another inconvenient result: few-shot prompting beat QLoRA within dataset v1.0, while QLoRA also had weak label-output reliability with test parse success around 0.435. During final evidence review I found that the classical and Gemma experiment families had been run on different dataset versions. Rather than hide that or rerun solely to manufacture a cleaner leaderboard, I published the version boundary and limited the claim accordingly. That research-governance decision is one of the strongest parts of the project.

## Hard questions ready

**What if QLoRA doesn’t help?**  
It didn't help in the controlled Gemma v1.0 comparison. Few-shot macro F1 was about 0.137 versus about 0.083 for QLoRA. That negative result is preserved rather than reframed as a win.

**Did TF-IDF beat Gemma?**  
The published numbers are much higher for TF-IDF, but they aren't a controlled cross-family comparison: the classical experiments use v1.1 and the Gemma experiments use v1.0. I report the scores descriptively and make the version boundary explicit.

**Isn’t this just schema reading?**  
Possibly in part, which is why the benchmark design and limitations are disclosed. The project is evidence-classification research, not proof that a small model understands real audit binders.

**Who reviewed the labels?**  
Primary labels are rule-derived. The challenge set has structural integrity auditing and a scripted narrative spot-check. I don't call the corpus an independently human-labeled gold standard.

**Is this an automated auditor?**  
No. ControlSift is a research and training artifact. Human judgment remains authoritative, and production audit replacement is explicitly out of scope.
