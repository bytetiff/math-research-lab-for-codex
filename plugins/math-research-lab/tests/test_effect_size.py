from math_research_lab.stats import cohen_d


def test_cohens_d_uses_pooled_standard_deviation():
    result = cohen_d([1, 2, 3, 4, 5, 6], ["a", "a", "a", "b", "b", "b"])
    assert result["mean_a"] == 2.0
    assert result["mean_b"] == 5.0
    assert result["cohens_d_b_minus_a"] > 2.0
    assert "pooled" in result["convention"]
