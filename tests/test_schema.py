import pytest
from pydantic import ValidationError

from controlsift.data.schema import MODEL_INPUT_FIELDS, EvidenceCase


def _valid_case(**overrides):
    base = {
        "id": "CS-TEST-0001",
        "scenario_family_id": "IAM-MFA-000",
        "variant_id": "A",
        "control_domain": "authentication",
        "control_statement": "Privileged accounts must use MFA.",
        "environment": "production identity platform",
        "evidence_type": "IAM enrollment export",
        "evidence_text": "Export shows MFA for all privileged accounts.",
        "label": "SUFFICIENT",
        "failure_tags": [],
        "difficulty": "easy",
        "generation_method": "synthetic_rule_based",
        "review_status": "unreviewed",
        "split": "train",
    }
    base.update(overrides)
    return base


def test_valid_case_parses():
    case = EvidenceCase.model_validate(_valid_case())
    assert case.label.value == "SUFFICIENT"
    assert set(case.model_input_dict()) == set(MODEL_INPUT_FIELDS)


def test_invalid_label_rejected():
    with pytest.raises(ValidationError):
        EvidenceCase.model_validate(_valid_case(label="GOOD_ENOUGH"))


def test_invalid_split_rejected():
    with pytest.raises(ValidationError):
        EvidenceCase.model_validate(_valid_case(split="holdout"))
