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
3. [Kaggle](https://www.kaggle.com/) account with phone verification if required for GPU.

## Package the repo without secrets

On your PC (from the repo root):

```bash
python scripts/package_for_kaggle.py
```

This writes `dist/controlsift_kaggle_bundle.zip` excluding `.env`, tokens, venvs, and git metadata.

Upload that zip as a **Kaggle Dataset** (private recommended) **or** clone from a public GitHub repo that contains no secrets.

## Kaggle notebook steps

1. Create notebook → Accelerator: **GPU**.
2. Add-ons → Secrets → add `HF_TOKEN` (value = your HF read token).
3. Attach the ControlSift dataset **or** clone the GitHub repo in the first cell.
4. Open / copy cells from [`kaggle_runner.ipynb`](kaggle_runner.ipynb).
5. Keep `SMOKE = True` for the first session (minutes).
6. If smoke passes, set `SMOKE = False` and re-run (uses weekly free GPU quota).
7. Download the produced `controlsift_gpu_outputs.zip`.
8. On your PC, unzip into the repo, then:

```bash
python scripts/run_evaluation.py
python scripts/build_figures.py
```

## What never leaves your machine

| Item | Where it lives |
|------|----------------|
| HF token | Kaggle/Colab secret store only |
| Kaggle API key | Local `~/.kaggle/kaggle.json` if you use CLI — gitignored |
| Employer / real audit data | Never — not part of this project |

## Free-quota tips

- Smoke first (`--limit`, `--smoke`).
- Prefer T4 + 4-bit QLoRA (already configured).
- If Kaggle GPU quota is exhausted, use Colab with the same notebook patterns and Colab Secrets.
