from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd


def _as_numeric(values: Sequence[float]) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        raise ValueError("at least one numeric value is required")
    if np.isnan(arr).any():
        raise ValueError("values must not contain NaN")
    return arr


def bootstrap_ci(
    values: Sequence[float],
    confidence: float = 0.95,
    resamples: int = 1000,
    seed: int = 0,
) -> dict[str, object]:
    '''Compute a deterministic bootstrap confidence interval for the mean.'''
    arr = _as_numeric(values)
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    if resamples <= 0:
        raise ValueError("resamples must be positive")
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, arr.size, size=(resamples, arr.size))
    means = arr[indices].mean(axis=1)
    alpha = 1.0 - confidence
    low, high = np.quantile(means, [alpha / 2.0, 1.0 - alpha / 2.0])
    return {
        "count": int(arr.size),
        "mean": float(arr.mean()),
        "std": float(arr.std(ddof=1)) if arr.size > 1 else 0.0,
        "confidence": confidence,
        "resamples": resamples,
        "seed": seed,
        "ci_low": float(low),
        "ci_high": float(high),
    }


def permutation_test(
    values: Sequence[float],
    groups: Sequence[str],
    permutations: int = 1000,
    seed: int = 0,
) -> dict[str, object]:
    '''Run a two-sided permutation test for difference of group means.'''
    arr = _as_numeric(values)
    labels = np.asarray(groups)
    if labels.size != arr.size:
        raise ValueError("groups length must match values length")
    unique = sorted({str(label) for label in labels})
    if len(unique) != 2:
        raise ValueError("exactly two groups are required")
    a, b = unique
    mask_b = labels.astype(str) == b
    observed = float(arr[mask_b].mean() - arr[~mask_b].mean())
    rng = np.random.default_rng(seed)
    count = 0
    for _ in range(permutations):
        shuffled = rng.permutation(labels)
        shuffled_b = shuffled.astype(str) == b
        diff = float(arr[shuffled_b].mean() - arr[~shuffled_b].mean())
        if abs(diff) >= abs(observed) - 1e-12:
            count += 1
    p_value = (count + 1.0) / (permutations + 1.0)
    return {
        "group_a": a,
        "group_b": b,
        "observed_difference_mean_b_minus_a": observed,
        "permutations": permutations,
        "seed": seed,
        "p_value_two_sided": float(p_value),
    }


def cohen_d(values: Sequence[float], groups: Sequence[str]) -> dict[str, object]:
    '''Compute Cohen's d using pooled sample standard deviation.'''
    arr = _as_numeric(values)
    labels = np.asarray(groups)
    if labels.size != arr.size:
        raise ValueError("groups length must match values length")
    unique = sorted({str(label) for label in labels})
    if len(unique) != 2:
        raise ValueError("exactly two groups are required")
    a, b = unique
    va = arr[labels.astype(str) == a]
    vb = arr[labels.astype(str) == b]
    if va.size < 2 or vb.size < 2:
        raise ValueError("each group needs at least two observations")
    pooled_var = ((va.size - 1) * va.var(ddof=1) + (vb.size - 1) * vb.var(ddof=1)) / (va.size + vb.size - 2)
    pooled = float(np.sqrt(pooled_var))
    d = float((vb.mean() - va.mean()) / pooled) if pooled > 0 else float("inf")
    return {
        "group_a": a,
        "group_b": b,
        "mean_a": float(va.mean()),
        "mean_b": float(vb.mean()),
        "cohens_d_b_minus_a": d,
        "convention": "difference of means divided by pooled sample standard deviation",
    }


def seed_sensitivity(frame: pd.DataFrame, seed_column: str, metric_column: str) -> dict[str, object]:
    '''Summarize metric sensitivity across seeds.'''
    if seed_column not in frame or metric_column not in frame:
        raise ValueError("seed and metric columns must exist")
    values = _as_numeric(frame[metric_column].to_numpy())
    mean = float(values.mean())
    std = float(values.std(ddof=1)) if values.size > 1 else 0.0
    result = {
        "seed_column": seed_column,
        "metric_column": metric_column,
        "num_observations": int(values.size),
        "num_unique_seeds": int(frame[seed_column].nunique()),
        "mean": mean,
        "std": std,
        "min": float(values.min()),
        "max": float(values.max()),
        "coefficient_of_variation": float(std / abs(mean)) if mean else None,
        "warnings": [],
    }
    if result["num_unique_seeds"] < 3:
        result["warnings"].append("Very small replication count; seed sensitivity is weakly estimated.")
    return result
