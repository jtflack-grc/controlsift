from controlsift import UNPARSEABLE
from controlsift.evaluation.parser import parse_model_output


def test_valid_json():
    out = parse_model_output('{"label": "PARTIAL", "rationale": "Coverage gap."}')
    assert out["label"] == "PARTIAL"
    assert out["parse_status"] == "json"


def test_embedded_json():
    text = 'Sure. Here you go:\n{"label": "CONTRADICTORY", "rationale": "MFA disabled."}\nThanks'
    out = parse_model_output(text)
    assert out["label"] == "CONTRADICTORY"


def test_bare_label():
    out = parse_model_output("INSUFFICIENT")
    assert out["label"] == "INSUFFICIENT"


def test_ambiguous_unparseable():
    out = parse_model_output("It could be PARTIAL or INSUFFICIENT depending on scope.")
    assert out["label"] == UNPARSEABLE


def test_empty():
    assert parse_model_output("")["label"] == UNPARSEABLE
