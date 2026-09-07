"""Smoke tests for MMC DeepMind weekly labs."""

from __future__ import annotations

from pathlib import Path

from mmc.labs import week01_ngram, week02_bpe, week04_mlp, week06_transformer, week07_lora_scaffold, week11_comparative
from mmc.labs.paths import OUT


def test_week01_ngram_writes_perplexity() -> None:
    log = week01_ngram.run()
    assert log["perplexity"] > 0
    assert (OUT / "week01_perplexity.json").is_file()


def test_week02_bpe_vocab() -> None:
    log = week02_bpe.run()
    assert log["vocab_size"] > 10
    assert (OUT / "week02_vocab.json").is_file()


def test_week04_mlp_learns_something() -> None:
    log = week04_mlp.run()
    assert log["test_accuracy"] >= 0.7
    assert (OUT / "week04_mlp_weights.npz").is_file()


def test_week06_attention_png() -> None:
    log = week06_transformer.run()
    assert Path(log["attention_png"]).is_file()


def test_week07_adapter_scaffold() -> None:
    log = week07_lora_scaffold.run()
    assert log["rank"] == 8
    assert (OUT / "week07_lora_adapter.npz").is_file()


def test_week11_comparative_includes_classical() -> None:
    log = week11_comparative.run()
    by_name = {r["experiment"]: r for r in log["rows"]}
    assert by_name["majority"]["test_macro_f1"] is not None
    assert by_name["tfidf"]["test_macro_f1"] is not None
    assert by_name["gemma_qlora"]["status"] == "pending_gpu"
    assert (OUT / "week11_comparative_analysis.json").is_file()
