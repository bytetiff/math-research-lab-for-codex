import numpy as np

from math_research_lab.spectral import effective_rank, spectral_entropy


def test_effective_rank_for_equal_spectrum():
    result = effective_rank(np.array([1.0, 1.0]), values_are_singular=True)
    assert abs(result["effective_rank"] - 2.0) < 1e-12
    entropy = spectral_entropy(np.array([1.0, 1.0]), values_are_singular=True)
    assert entropy["normalized_spectral_entropy"] == 1.0
