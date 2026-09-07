"""Week 1 deliverable: n-gram LM + perplexity logs."""

from __future__ import annotations

import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

from mmc.labs.paths import CORPUS, ensure_out


def tokenize(text: str) -> list[str]:
    return text.lower().replace(".", " .").replace(",", " ,").split()


class NGramLM:
    def __init__(self, n: int = 3) -> None:
        self.n = n
        self.ngrams: dict[tuple[str, ...], Counter[str]] = defaultdict(Counter)
        self.unigrams: Counter[str] = Counter()

    def fit(self, tokens: list[str]) -> None:
        self.unigrams.update(tokens)
        if len(tokens) < self.n:
            return
        for i in range(len(tokens) - self.n + 1):
            ctx = tuple(tokens[i : i + self.n - 1])
            nxt = tokens[i + self.n - 1]
            self.ngrams[ctx][nxt] += 1

    def _prob(self, ctx: tuple[str, ...], token: str) -> float:
        counts = self.ngrams.get(ctx)
        if counts and sum(counts.values()) > 0:
            return (counts[token] + 1.0) / (sum(counts.values()) + len(self.unigrams))
        # backoff to unigram add-one
        return (self.unigrams[token] + 1.0) / (sum(self.unigrams.values()) + len(self.unigrams))

    def perplexity(self, tokens: list[str]) -> float:
        if len(tokens) < self.n:
            return float("inf")
        log_sum = 0.0
        n_pred = 0
        for i in range(self.n - 1, len(tokens)):
            ctx = tuple(tokens[i - self.n + 1 : i])
            p = max(self._prob(ctx, tokens[i]), 1e-12)
            log_sum += math.log(p)
            n_pred += 1
        return math.exp(-log_sum / n_pred)

    def generate(self, max_tokens: int = 40, seed: int = 42) -> str:
        rng = random.Random(seed)
        if not self.ngrams:
            return ""
        ctx = list(rng.choice(list(self.ngrams.keys())))
        out = list(ctx)
        for _ in range(max_tokens):
            counts = self.ngrams.get(tuple(ctx))
            if not counts:
                break
            tokens, weights = zip(*counts.items())
            nxt = rng.choices(list(tokens), weights=list(weights), k=1)[0]
            out.append(nxt)
            ctx = (ctx + [nxt])[-(self.n - 1) :]
        return " ".join(out)


def run(corpus_path: Path | None = None) -> dict:
    out = ensure_out()
    text = (corpus_path or CORPUS).read_text(encoding="utf-8")
    tokens = tokenize(text)
    split = int(0.8 * len(tokens))
    train, test = tokens[:split], tokens[split:]
    model = NGramLM(n=3)
    model.fit(train)
    ppl = model.perplexity(test if len(test) >= 3 else train)
    sample = model.generate()
    log = {
        "deliverable": "week01_ngram",
        "n": 3,
        "train_tokens": len(train),
        "test_tokens": len(test),
        "vocab_size": len(model.unigrams),
        "perplexity": ppl,
        "sample_generation": sample,
    }
    (out / "week01_perplexity.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
    (out / "week01_sample.txt").write_text(sample + "\n", encoding="utf-8")
    return log


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
