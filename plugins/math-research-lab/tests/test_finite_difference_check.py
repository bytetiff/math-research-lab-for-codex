from math_research_lab.numerics import central_difference, finite_difference_report


def test_central_finite_difference_matches_quadratic_derivative():
    estimate = central_difference(lambda x: x * x, 3.0, step=1e-6)
    assert abs(estimate - 6.0) < 1e-5
    report = finite_difference_report(lambda x: x * x, 3.0, expected=6.0, step=1e-6, tolerance=1e-5)
    assert report["passed"] is True
