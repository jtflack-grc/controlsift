"""Family-level split assignment — no scenario family may cross partitions (§19)."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from typing import Iterable, Sequence

from controlsift import CANONICAL_SEED

SPLIT_TARGETS = {
    "train": 1000,
    "validation": 200,
    "test": 200,
    "challenge": 100,
}


def _stable_rank(family_id: str, seed: int = CANONICAL_SEED) -> int:
    digest = hashlib.sha256(f"{seed}:{family_id}".encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def assign_family_splits(
    family_ids: Sequence[str],
    *,
    seed: int = CANONICAL_SEED,
    train_frac: float = 1000 / 1500,
    val_frac: float = 200 / 1500,
    test_frac: float = 200 / 1500,
) -> dict[str, str]:
    """Assign each unique scenario_family_id to exactly one split.

    Challenge receives the remaining fraction (~100/1500).
    Assignment is deterministic given seed and family id set.
    """
    unique = sorted(set(family_ids))
    ranked = sorted(unique, key=lambda fid: _stable_rank(fid, seed))
    n = len(ranked)
    if n == 0:
        return {}

    n_train = max(1, int(round(n * train_frac)))
    n_val = max(1, int(round(n * val_frac)))
    n_test = max(1, int(round(n * test_frac)))
    # Ensure totals fit
    while n_train + n_val + n_test >= n and n_train > 1:
        n_train -= 1
    while n_train + n_val + n_test >= n and n_val > 1:
        n_val -= 1
    while n_train + n_val + n_test >= n and n_test > 1:
        n_test -= 1
    n_challenge = n - (n_train + n_val + n_test)
    if n_challenge < 1:
        # Steal one from train for challenge when family count is tiny (unit tests).
        n_train = max(1, n_train - 1)
        n_challenge = n - (n_train + n_val + n_test)

    assignment: dict[str, str] = {}
    i = 0
    for fid in ranked[i : i + n_train]:
        assignment[fid] = "train"
    i += n_train
    for fid in ranked[i : i + n_val]:
        assignment[fid] = "validation"
    i += n_val
    for fid in ranked[i : i + n_test]:
        assignment[fid] = "test"
    i += n_test
    for fid in ranked[i:]:
        assignment[fid] = "challenge"
    return assignment


def apply_splits(
    cases: Iterable[dict],
    family_to_split: dict[str, str],
) -> list[dict]:
    out: list[dict] = []
    for case in cases:
        fid = case["scenario_family_id"]
        if fid not in family_to_split:
            raise KeyError(f"No split assignment for family {fid}")
        updated = dict(case)
        updated["split"] = family_to_split[fid]
        out.append(updated)
    return out


def detect_family_leakage(cases: Iterable[dict]) -> list[str]:
    """Return family ids that appear in more than one split."""
    family_splits: dict[str, set[str]] = defaultdict(set)
    for case in cases:
        family_splits[case["scenario_family_id"]].add(case["split"])
    return sorted(fid for fid, splits in family_splits.items() if len(splits) > 1)
