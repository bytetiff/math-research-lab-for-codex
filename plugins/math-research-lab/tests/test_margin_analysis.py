import numpy as np

from math_research_lab.geometry import margin_analysis, margins


def test_margin_calculation_and_boundary_crossing():
    before = np.array([[0.0, 1.0], [2.0, 1.0], [0.0, 2.0]])
    after = np.array([[2.0, 1.0], [1.0, 3.0], [0.0, 2.0]])
    labels = np.array([0, 0, 1])
    assert margins(after, labels).tolist() == [1.0, -2.0, 2.0]
    result = margin_analysis(after, labels, before_logits=before)
    assert result["before_after"]["negative_to_positive_crossing_rate"] == 1 / 3
    assert result["before_after"]["positive_to_negative_crossing_rate"] == 1 / 3
    assert result["before_after"]["num_prediction_flips"] == 2
