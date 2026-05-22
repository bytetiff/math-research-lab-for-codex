import numpy as np

from math_research_lab.geometry import pairwise_distance_summary


def test_pairwise_distance_summary():
    features = np.array([[0, 0], [3, 4], [0, 4]], dtype=float)
    result = pairwise_distance_summary(features)
    assert result["num_vectors"] == 3
    assert result["dimension"] == 2
    assert result["min"] == 3.0
    assert result["max"] == 5.0
    assert result["mean"] == 4.0
