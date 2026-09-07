from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MMC = ROOT / "mmc"
OUT = MMC / "deliverables" / "outputs"
CORPUS = MMC / "labs" / "sample_corpus.txt"
DOCS_DELIV = ROOT / "docs" / "capstone" / "deliverables"


def ensure_out() -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    return OUT
