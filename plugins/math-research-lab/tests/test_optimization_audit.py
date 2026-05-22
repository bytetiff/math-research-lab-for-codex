from math_research_lab.optimization import convergence_diagnostics


def test_convergence_diagnostics_uses_correct_nondecreasing_key():
    result = convergence_diagnostics([1.0, 2.0, 2.0, 3.0])
    assert result["monotone_nondecreasing"] is True
    assert result["monotone_nondecresing"] is True
