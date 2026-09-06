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

If accelerators are greyed out in a new notebook: Settings → Phone Verification → SMS code → refresh the notebook → right sidebar **Session options** → Accelerator.

### Optional local CLI (controlsift-mmc conda env)

```powershell
conda activate controlsift-mmc
kaggle auth login
# or place API token per Kaggle settings (never commit it)
```

The Kaggle CLI is for dataset upload convenience. The GPU run itself still happens in a Kaggle **Notebook** with `HF_TOKEN` in Secrets.
## Before you touch accounts

- Dataset **v1.1.0** is sealed under tag `protocol-v1-locked`.
- Evidence texts are **compositional packets** (dual sections / `SCOPE` / substance pointer). The frozen prompt does **not** explain that grammar — measure discovery, do not “fix” the prompt against the test set.
- Public classical receipts: majority macro F1 ≈ 0.067, TF-IDF ≈ 0.53 test. Gemma slots stay `null` until you write `results/gemma_*`.

## Package the repo without secrets

On your PC (from the repo root):

```bash
python scripts/package_for_kaggle.py
```

This writes `dist/controlsift_kaggle_bundle.zip` excluding `.env`, tokens, venvs, and git metadata. Confirm the zip lists `controlsift/data/processed/*.jsonl`, `controlsift/notebooks/kaggle_runner.ipynb`, and `controlsift/configs/`.

Upload that zip as a **Kaggle Dataset** (private recommended) **or** clone from a public GitHub repo that contains no secrets.

## Kaggle notebook steps

1. Create notebook → Accelerator: **GPU**.
2. Add-ons → Secrets → add `HF_TOKEN` (value = your HF read token).
3. Attach the ControlSift dataset **or** clone the GitHub repo in the first cell.
4. Open / copy cells from [`kaggle_runner.ipynb`](kaggle_runner.ipynb).
5. Keep `SMOKE = True` for the first session (minutes).
6. If smoke passes, set `SMOKE = False` and re-run (uses weekly free GPU quota).
7. Download the produced `controlsift_gpu_outputs.zip`.
8. On your PC (from the repo root):

```powershell
python scripts/after_kaggle.py --zip "$env:USERPROFILE\Downloads\controlsift_gpu_outputs.zip"
```

That extracts `results/` safely (skips weight blobs), then refreshes `docs/data/results.json`, figures, Week 11 comparative JSON, and the deliverables hub sync.
## What never leaves your machine

| Item | Where it lives |
|------|----------------|
| HF token | Kaggle/Colab secret store only |
| Kaggle API key | Local `~/.kaggle/kaggle.json` if you use CLI — gitignored |
| Employer / real audit data | Never — not part of this project |

## Gemma 3 dependency note

Gemma 3 requires **transformers ≥ 4.50**. The runner install cell upgrades it explicitly before `pip install -e ".[gpu]"`. If you uploaded an older Dataset version, either publish a new Dataset version from the latest `dist/controlsift_kaggle_bundle.zip`, or run:

```
!pip -q install -U "transformers>=4.50"
```

before the rest of the notebook.

**torchao / peft:** peft ≥ 0.16 rejects installed `torchao` &lt; 0.16 (common Kaggle preinstall is 0.10). The Install cell runs `pip install -U "torchao>=0.16"` and uninstalls torchao if upgrade fails. Eval/baseline scripts also preflight this.

**Locate preserves `results/`:** re-cloning no longer wipes a successful smoke-train adapter. After a torchao fix push: **Locate → Install → QLoRA eval → Package** (skip train if `results/gemma_qlora/adapter` still exists).

## Colab fallback (if Kaggle accelerators stay greyed out)

1. Phone-verify Kaggle first if you can — prefer Kaggle for the weekly GPU quota.
2. Else open [Google Colab](https://colab.research.google.com/) → Runtime → Change runtime type → **GPU**.
3. Secrets (key icon) → add `HF_TOKEN`.
4. Upload `notebooks/kaggle_runner.ipynb` (File → Upload) **or** open from Drive.
5. Run the Colab bootstrap cell and upload `dist/controlsift_kaggle_bundle.zip` when prompted.
6. Keep `SMOKE = True` first; then `SMOKE = False` for public metrics.
7. Download `controlsift_gpu_outputs.zip` → same `after_kaggle.py --zip …` on your PC.

## Free-quota tips

- Smoke first (`--limit`, `--smoke`).
- Prefer T4 + 4-bit QLoRA (already configured).
- If Kaggle GPU quota is exhausted **or** accelerators are locked pending phone verification, use Colab with the steps above.
