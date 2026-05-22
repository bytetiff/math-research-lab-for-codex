from math_research_lab.stats import bootstrap_ci


def test_bootstrap_ci_is_deterministic_with_seed():
    values = [1, 2, 3, 4, 5]
    first = bootstrap_ci(values, resamples=200, seed=7)
    second = bootstrap_ci(values, resamples=200, seed=7)
    assert first == second
    assert first["mean"] == 3.0
    assert first["ci_low"] <= first["mean"] <= first["ci_high"]
