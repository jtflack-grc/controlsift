from pathlib import Path

import pytest

from controlsift.data.generate import generate_dataset
from controlsift.data.split import detect_family_leakage
from controlsift.data.validate import load_all_splits, validate_dataset

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def generated(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("data")
    processed = tmp / "processed"
    manifest = tmp / "manifest.json"
    review = tmp / "review_log.csv"
    generate_dataset(
        scenarios_path=ROOT / "data" / "scenarios" / "scenario_families.yaml",
        out_dir=processed,
        manifest_path=manifest,
        review_path=review,
        seed=42,
        adversarial=False,  # full AFLite pass is covered by committed data + lexical ceiling test
    )
    return processed


def test_validate_passes(generated):
    report = validate_dataset(generated)
    assert report["ok"] is True
    assert report["total_cases"] == 1500


def test_no_family_leakage(generated):
    cases = load_all_splits(generated)
    assert detect_family_leakage(cases) == []
