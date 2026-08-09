# Interview Narrative — ControlSift

## 60 seconds

ControlSift asks whether a small model can tell proof from paperwork in cybersecurity evidence. I built a synthetic benchmark, locked a research protocol, ran classical and Gemma baselines, and adapted Gemma with QLoRA — then evaluated on sealed test and challenge sets with an explicit Failure Lab for remaining errors.

## Five minutes

Most “fine-tuning demos” stop at a loss curve. I treated this as AI assurance: family-isolated splits, TF-IDF as a lexical shortcut detector (it initially scored 1.0, so I hardened the data), protocol seal before final testing, and public metrics that stay null until real JSON exists. The career artifact is not “I fine-tuned Gemma”; it is “I can tell whether adaptation helped and where it still fails.”

## Hard question ready

**What if QLoRA doesn’t help?**  
That’s still a valid result. The project preserves negative findings and emphasizes challenge-set generalization and error analysis over vanity metrics.
