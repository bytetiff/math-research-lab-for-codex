import numpy as np

from math_research_lab.geometry import prototype_geometry


def test_prototype_geometry_computes_prototypes_and_variance():
    features = np.array([[0, 0], [2, 0], [10, 0], [12, 0]], dtype=float)
    labels = np.array([0, 0, 1, 1])
    result = prototype_geometry(features, labels)
    assert result["prototypes"]["0"] == [1.0, 0.0]
    assert result["prototypes"]["1"] == [11.0, 0.0]
    assert result["inter_prototype_distances"][0]["distance"] == 10.0
    assert result["intra_class_variance"]["0"] == 1.0
