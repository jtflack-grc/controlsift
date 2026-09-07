# MMC show-work notebooks

Thin notebooks that check DeepMind / MMC week boxes using ControlSift artifacts.  
Map: [`../GDM_LAB_MAP.md`](../GDM_LAB_MAP.md) · Official labs: [`../../vendor/ai-foundations/`](../../vendor/ai-foundations/)

## Local (recommended): Anaconda

```powershell
cd C:\Users\admin\Desktop\sifter
conda env create -f environment-mmc.yml   # once
conda activate controlsift-mmc
powershell -File scripts\start_mmc_jupyter.ps1
```

Kernel name: **Python (controlsift-mmc)**. Run cells top-to-bottom.

Headless smoke test:

```powershell
conda activate controlsift-mmc
python scripts\execute_mmc_notebooks.py
```

## Browser after GitHub / GitHub Pages

| Host | Runs Python? | Role |
|------|--------------|------|
| **GitHub Pages** | No (static only) | Hub + artifact viewers |
| **Local Jupyter / Anaconda** | Yes | Best path for writing `mmc/deliverables/outputs/` |
| **Google Colab** | Yes | Browser run after repo is on GitHub |
| **Binder** | Yes (CPU) | Temporary cloud Jupyter from GitHub |

Set `github_slug` in `docs/data/repo.json` after push. Hub buttons then point at:

- Colab: `https://colab.research.google.com/github/OWNER/REPO/blob/main/mmc/notebooks/week01_ngram.ipynb`
- Binder: `https://mybinder.org/v2/gh/OWNER/REPO/main?urlpath=lab/tree/mmc/notebooks/week01_ngram.ipynb`

## Notebook index

| Notebook | Title |
|----------|-------|
| `week01_ngram.ipynb` | Week 1 — N-gram LM + perplexity |
| `week02_bpe.ipynb` | Week 2 — BPE |
| `week04_mlp.ipynb` | Week 4 — MLP |
| `week05_diagnostics.ipynb` | Week 5 — Diagnostics |
| `week06_transformer.ipynb` | Week 6 — Transformer |
| `week07_lora.ipynb` | Week 7 — LoRA |
| `week09_accelerate.ipynb` | Week 9 — Accelerate notes |
| `week11_comparative.ipynb` | Week 11 — Comparative |
