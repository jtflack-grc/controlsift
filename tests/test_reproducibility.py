from pathlib import Path

from controlsift import CANONICAL_SEED
from controlsift.data.generate import generate_cases, load_scenario_families

SCENARIOS = Path(__file__).resolve().parents[1] / "data" / "scenarios" / "scenario_families.yaml"


def test_generation_deterministic():
    families = load_scenario_families(SCENARIOS)
    a = generate_cases(families, seed=CANONICAL_SEED)
    b = generate_cases(families, seed=CANONICAL_SEED)
    assert [c["id"] for c in a] == [c["id"] for c in b]
    assert [c["evidence_text"] for c in a] == [c["evidence_text"] for c in b]
    assert len(a) == 1500
