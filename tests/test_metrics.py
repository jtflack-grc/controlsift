from controlsift.evaluation.metrics import (
    compute_classification_metrics,
    majority_baseline_predictions,
)


def test_perfect_macro_f1():
    y = ["SUFFICIENT", "PARTIAL", "INSUFFICIENT", "IRRELEVANT", "CONTRADICTORY"]
    m = compute_classification_metrics(y, y)
    assert m["macro_f1"] == 1.0
    assert m["parse_success_rate"] == 1.0


def test_unparseable_hurts_score():
    y = ["SUFFICIENT", "PARTIAL"]
    p = ["SUFFICIENT", "UNPARSEABLE"]
    m = compute_classification_metrics(y, p)
    assert m["macro_f1"] < 1.0
    assert m["parse_success_rate"] == 0.5


def test_majority_predictions():
    preds = majority_baseline_predictions(["A", "A", "B"], 4)
    assert preds == ["A", "A", "A", "A"]
