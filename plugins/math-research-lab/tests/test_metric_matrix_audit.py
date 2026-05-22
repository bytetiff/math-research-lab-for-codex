import pandas as pd

from math_research_lab.metrics import audit_metric_matrix


def test_metric_matrix_reconstruction_duplicates_and_missing_diagonal():
    df = pd.DataFrame({
        "row": [0, 0, 0, 1, 2],
        "col": [0, 1, 1, 0, 1],
        "value": [1.0, 2.0, 2.5, 3.0, 4.0],
    })
    result = audit_metric_matrix(df)
    assert result["shape"] == [3, 2]
    assert result["duplicate_cells"][0]["row"] == 0
    assert result["duplicate_cells"][0]["col"] == 1
    assert result["missing_diagonal"] == [1, 2]
    assert result["inconsistent_index_ranges"] is True
