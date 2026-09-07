"""Week 2 deliverable: custom BPE tokenizer + vocabulary export."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from mmc.labs.paths import CORPUS, ensure_out


def word_freqs(text: str) -> Counter[str]:
    words = re.findall(r"[A-Za-z0-9]+|[^\sA-Za-z0-9]", text.lower())
    return Counter(words)


def train_bpe(text: str, num_merges: int = 40) -> tuple[list[tuple[str, str]], dict[str, int]]:
    freqs = word_freqs(text)
    splits: dict[str, list[str]] = {w: list(w) + ["</w>"] for w in freqs}
    merges: list[tuple[str, str]] = []
    vocab: dict[str, int] = {}

    def recompute_vocab() -> None:
        vocab.clear()
        i = 0
        for syms in splits.values():
            for s in syms:
                if s not in vocab:
                    vocab[s] = i
                    i += 1

    recompute_vocab()
    for _ in range(num_merges):
        pair_counts: Counter[tuple[str, str]] = Counter()
        for word, freq in freqs.items():
            syms = splits[word]
            for i in range(len(syms) - 1):
                pair_counts[(syms[i], syms[i + 1])] += freq
        if not pair_counts:
            break
        best = pair_counts.most_common(1)[0][0]
        merges.append(best)
        bigram = best[0] + best[1]
        for word in list(splits):
            syms = splits[word]
            i = 0
            new: list[str] = []
            while i < len(syms):
                if i < len(syms) - 1 and syms[i] == best[0] and syms[i + 1] == best[1]:
                    new.append(bigram)
                    i += 2
                else:
                    new.append(syms[i])
                    i += 1
            splits[word] = new
        recompute_vocab()
    return merges, vocab


def encode(text: str, merges: list[tuple[str, str]]) -> list[str]:
    tokens: list[str] = []
    for word in re.findall(r"[A-Za-z0-9]+|[^\sA-Za-z0-9]", text.lower()):
        syms = list(word) + ["</w>"]
        for a, b in merges:
            i = 0
            new: list[str] = []
            while i < len(syms):
                if i < len(syms) - 1 and syms[i] == a and syms[i + 1] == b:
                    new.append(a + b)
                    i += 2
                else:
                    new.append(syms[i])
                    i += 1
            syms = new
        tokens.extend(syms)
    return tokens


def run(corpus_path: Path | None = None) -> dict:
    out = ensure_out()
    text = (corpus_path or CORPUS).read_text(encoding="utf-8")
    merges, vocab = train_bpe(text, num_merges=50)
    sample_tokens = encode(text.splitlines()[0], merges)
    payload = {
        "deliverable": "week02_bpe",
        "num_merges": len(merges),
        "vocab_size": len(vocab),
        "sample_line_tokens": sample_tokens,
        "data_card": "governance/DATA_CARD.md",
        "controlsift_data_card_html": "docs/assurance/data-card.html",
    }
    (out / "week02_merges.json").write_text(json.dumps(merges, indent=2), encoding="utf-8")
    (out / "week02_vocab.json").write_text(json.dumps(vocab, indent=2), encoding="utf-8")
    (out / "week02_summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
