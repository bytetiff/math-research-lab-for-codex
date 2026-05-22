import numpy as np

from math_research_lab.spectral import svd_energy


def test_svd_energy_retained_energy():
    matrix = np.diag([3.0, 4.0])
    result = svd_energy(matrix, rank=1)
    assert result["singular_values"] == [4.0, 3.0]
    assert result["retained_energy"] == 16 / 25
