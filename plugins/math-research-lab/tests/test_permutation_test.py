from math_research_lab.stats import permutation_test


def test_permutation_test_detects_separated_groups():
    result = permutation_test([1, 1, 1, 10, 10, 10], ["a", "a", "a", "b", "b", "b"], permutations=999, seed=1)
    assert result["observed_difference_mean_b_minus_a"] == 9.0
    assert result["p_value_two_sided"] < 0.2


def test_permutation_test_non_separated_groups_high_p_value():
    result = permutation_test([1, 2, 1, 2, 1, 2], ["a", "a", "a", "b", "b", "b"], permutations=999, seed=1)
    assert result["p_value_two_sided"] > 0.5
