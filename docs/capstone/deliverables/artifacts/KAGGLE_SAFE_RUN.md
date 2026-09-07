# Safe free GPU run (Kaggle / Colab)

This guide keeps ControlSift **free**, **local-secret-only**, and **non-exposing**.

## Security rules (non-negotiable)

1. **Never paste** a Hugging Face token, Kaggle key, or password into a notebook cell, chat, README, or git commit.
2. Store the HF token only in **Kaggle Secrets** or **Colab Secrets** as `HF_TOKEN`.
3. Do **not** enable “share notebook with secrets” or publish a notebook that has already printed auth errors containing tokens.
4. Download only `results/` JSON/JSONL (+ small `training_meta.json`). Prefer **not** uploading full `.safetensors` adapters to a public repo unless you intend to.
5. The benchmark is **synthetic** — still do not upload employer/customer evidence to Kaggle.

## One-time accounts

1. [Hugging Face](https://huggingface.co/) → accept license for [`google/gemma-3-1b-it`](https://huggingface.co/google/gemma-3-1b-it).
2. Create a **read** access token (Settings → Access Tokens).
3. [Kaggle](https://www.kaggle.com/) account with **phone verification** (required before GPU/TPU accelerators unlock).

If accelerators are greyed out: Settings → Phone Verification → SMS code → refresh the notebook → Session options → Accelerator.

## Before you run

- Dataset **v1.1.0** is sealed under tag `protocol-v1-locked`.
- Evidence texts are compositional packets; the frozen prompt does **not** explain that grammar — measure discovery, do not tune the prompt against the test set.
- Classical receipts (TEST macro F1): majority ≈ 0.067, TF-IDF ≈ 0.533. Gemma ladder scores live in `docs/data/results.json` after a full GPU merge.

## Package the repo without secrets

```bash
python scripts/package_for_kaggle.py
```

This writes `dist/controlsift_kaggle_bundle.zip` excluding `.env`, tokens, venvs, and git metadata.

## Kaggle notebook steps

1. Create notebook → Accelerator: **GPU** · Internet **ON**.
2. Add-ons → Secrets → add `HF_TOKEN`.
3. Upload / open [`kaggle_runner.ipynb`](https://github.com/jtflack-grc/controlsift/raw/kaggle-bundle/notebooks/kaggle_runner.ipynb).
4. Keep `SMOKE = True` for the first session (minutes).
5. If smoke passes, set `SMOKE = False` and re-run (uses weekly free GPU quota).
6. Download `controlsift_gpu_outputs.zip`.
7. On your PC:

```powershell
python scripts/after_kaggle.py --zip "$env:USERPROFILE\Downloads\controlsift_gpu_outputs.zip"
```

That extracts `results/` safely (skips weight blobs), then refreshes `docs/data/results.json`, figures, and deliverables sync.

## What never leaves your machine

| Item | Where it lives |
|------|----------------|
| HF token | Kaggle/Colab secret store only |
| Kaggle API key | Local `~/.kaggle/kaggle.json` if you use CLI — gitignored |
| Employer / real audit data | Never — not part of this project |

## Dependency notes

- Gemma 3 needs **transformers ≥ 4.50** (install cell upgrades it).
- Prefer T4 + 4-bit QLoRA (already configured in the runner).

## Colab fallback

1. Prefer Kaggle when GPU is unlocked.
2. Else [Colab](https://colab.research.google.com/) → Runtime → GPU → upload `kaggle_runner.ipynb` → Secrets `HF_TOKEN`.
3. `SMOKE = True` first; then `False` for public metrics.
4. Download zip → same `after_kaggle.py` merge on your PC.

See also: [kaggle-checklist.html](../kaggle-checklist.html) · [AFTER_GPU.md](AFTER_GPU.md) · [colab-checklist.html](../colab-checklist.html).
