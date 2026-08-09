from controlsift.data.split import assign_family_splits, detect_family_leakage


def test_family_assigned_to_exactly_one_split():
    families = [f"FAM-{i:03d}" for i in range(60)]
    assignment = assign_family_splits(families, seed=42)
    assert set(assignment) == set(families)
    assert all(s in {"train", "validation", "test", "challenge"} for s in assignment.values())
    # All four splits present for reasonably large N
    assert len(set(assignment.values())) == 4


def test_detect_family_leakage():
    cases = [
        {"scenario_family_id": "A", "split": "train"},
        {"scenario_family_id": "A", "split": "test"},
        {"scenario_family_id": "B", "split": "train"},
    ]
    assert detect_family_leakage(cases) == ["A"]


def test_no_leakage_when_consistent():
    cases = [
        {"scenario_family_id": "A", "split": "train"},
        {"scenario_family_id": "A", "split": "train"},
        {"scenario_family_id": "B", "split": "test"},
    ]
    assert detect_family_leakage(cases) == []


def test_assignment_deterministic():
    families = [f"FAM-{i:03d}" for i in range(100)]
    a = assign_family_splits(families, seed=42)
    b = assign_family_splits(families, seed=42)
    assert a == b
