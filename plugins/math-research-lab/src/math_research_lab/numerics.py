from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

import numpy as np

from .safe_expr import evaluate_expression


@dataclass(frozen=True)
class FiniteDifferenceResult:
    '''Result of a scalar central finite-difference check.'''

    point: float
    estimate: float
    expected: float | None
    absolute_error: float | None
    tolerance: float
    passed: bool | None

    def to_dict(self) -> dict[str, float | bool | None]:
        return {
            "point": self.point,
            "estimate": self.estimate,
            "expected": self.expected,
            "absolute_error": self.absolute_error,
            "tolerance": self.tolerance,
            "passed": self.passed,
        }


def central_difference(function: Callable[[float], float], point: float, step: float = 1e-5) -> float:
    '''Compute a scalar central finite difference.'''
    if step <= 0:
        raise ValueError("step must be positive")
    return float((function(point + step) - function(point - step)) / (2.0 * step))


def finite_difference_report(
    function: Callable[[float], float],
    point: float,
    expected: float | None = None,
    step: float = 1e-5,
    tolerance: float = 1e-4,
) -> dict[str, float | bool | None | str]:
    '''Return a finite-difference report without interpreting mathematical validity beyond the check.'''
    estimate = central_difference(function, point, step)
    error = None if expected is None else abs(estimate - expected)
    passed = None if error is None else error <= tolerance
    result = FiniteDifferenceResult(point, estimate, expected, error, tolerance, passed).to_dict()
    result["note"] = "A finite-difference match is a numerical consistency check, not a proof."
    return result


def gradient_check(
    function: Callable[[np.ndarray], float],
    analytic_gradient: Callable[[np.ndarray], np.ndarray],
    point: Sequence[float],
    step: float = 1e-5,
    tolerance: float = 1e-4,
) -> dict[str, object]:
    '''Compare an analytic gradient with central finite differences.'''
    if step <= 0:
        raise ValueError("step must be positive")
    x = np.asarray(point, dtype=float)
    analytic = np.asarray(analytic_gradient(x), dtype=float)
    if analytic.shape != x.shape:
        raise ValueError("analytic gradient must have the same shape as point")
    numerical = np.zeros_like(x)
    for idx in range(x.size):
        plus = x.copy()
        minus = x.copy()
        plus[idx] += step
        minus[idx] -= step
        numerical[idx] = (function(plus) - function(minus)) / (2.0 * step)
    max_abs_error = float(np.max(np.abs(numerical - analytic))) if x.size else 0.0
    return {
        "point": x.tolist(),
        "analytic_gradient": analytic.tolist(),
        "numerical_gradient": numerical.tolist(),
        "max_absolute_error": max_abs_error,
        "tolerance": tolerance,
        "passed": bool(max_abs_error <= tolerance),
        "note": "Gradient checks validate local numerical consistency only.",
    }


def randomized_property_test(
    predicate: Callable[[np.ndarray], bool],
    dimension: int,
    low: float = -1.0,
    high: float = 1.0,
    trials: int = 100,
    seed: int = 0,
) -> dict[str, object]:
    '''Run seeded random property checks for a callable predicate.'''
    if dimension <= 0:
        raise ValueError("dimension must be positive")
    if trials <= 0:
        raise ValueError("trials must be positive")
    rng = np.random.default_rng(seed)
    failures: list[dict[str, object]] = []
    for trial in range(trials):
        sample = rng.uniform(low, high, size=dimension)
        try:
            ok = bool(predicate(sample))
        except Exception as exc:  # pragma: no cover - defensive path
            failures.append({"trial": trial, "sample": sample.tolist(), "error": str(exc)})
            continue
        if not ok:
            failures.append({"trial": trial, "sample": sample.tolist()})
    return {
        "trials": trials,
        "seed": seed,
        "failures": failures,
        "passed": not failures,
        "note": "Passing randomized tests is not proof; it only reports no sampled counterexample.",
    }


def search_counterexamples_expression(
    expression: str,
    variables: list[str],
    low: float = -1.0,
    high: float = 1.0,
    trials: int = 1000,
    seed: int = 0,
) -> dict[str, object]:
    '''Search for randomized counterexamples to a restricted boolean expression.'''
    if not variables:
        raise ValueError("at least one variable is required")
    rng = np.random.default_rng(seed)
    counterexamples: list[dict[str, float]] = []
    for _ in range(trials):
        values = {name: float(rng.uniform(low, high)) for name in variables}
        if not bool(evaluate_expression(expression, values)):
            counterexamples.append(values)
            break
    return {
        "expression": expression,
        "variables": variables,
        "trials": trials,
        "seed": seed,
        "counterexample": counterexamples[0] if counterexamples else None,
        "note": "No counterexample found is not proof of the predicate.",
    }


def stability_summary(values: Sequence[float], groups: Sequence[str] | None = None) -> dict[str, object]:
    '''Summarize numeric stability overall and, when provided, by group.'''
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        raise ValueError("at least one value is required")
    result: dict[str, object] = {
        "count": int(arr.size),
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr, ddof=1)) if arr.size > 1 else 0.0,
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
    }
    if groups is not None:
        if len(groups) != arr.size:
            raise ValueError("groups length must match values length")
        grouped: dict[str, list[float]] = {}
        for group, value in zip(groups, arr):
            grouped.setdefault(str(group), []).append(float(value))
        result["groups"] = {key: stability_summary(vals) for key, vals in grouped.items()}
    return result


def verify_sympy_identity(lhs: str, rhs: str, variables: list[str]) -> dict[str, object]:
    '''Verify a symbolic identity using SymPy when available.'''
    try:
        import sympy as sp
    except ImportError as exc:  # pragma: no cover - depends on optional runtime package
        raise RuntimeError("SymPy is required for symbolic identity checks") from exc
    symbols = {name: sp.symbols(name) for name in variables}
    try:
        lhs_expr = sp.sympify(lhs, locals=symbols)
        rhs_expr = sp.sympify(rhs, locals=symbols)
    except Exception as exc:
        raise ValueError(f"Could not parse SymPy expression: {exc}") from exc
    residual = sp.simplify(lhs_expr - rhs_expr)
    return {
        "lhs": lhs,
        "rhs": rhs,
        "variables": variables,
        "simplified_residual": str(residual),
        "verdict": "identity" if residual == 0 else "not_simplified_to_zero",
        "note": "SymPy simplification is useful evidence but not a complete proof system for every expression class.",
    }
