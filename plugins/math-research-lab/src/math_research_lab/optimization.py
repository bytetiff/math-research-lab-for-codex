from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd


def loss_curve_audit(frame: pd.DataFrame, step_col: str, loss_col: str) -> dict[str, object]:
    '''Detect simple missing-step, spike, plateau, and instability signals in a loss curve.'''
    if step_col not in frame or loss_col not in frame:
        raise ValueError("step and loss columns must exist")
    ordered = frame[[step_col, loss_col]].sort_values(step_col)
    steps = ordered[step_col].to_numpy(dtype=float)
    losses = ordered[loss_col].to_numpy(dtype=float)
    diffs = np.diff(losses)
    step_diffs = np.diff(steps)
    expected_step = float(np.median(step_diffs)) if step_diffs.size else 0.0
    missing_steps = int(np.sum(step_diffs > expected_step * 1.5)) if expected_step > 0 else 0
    spike_threshold = float(np.mean(diffs) + 3 * np.std(diffs)) if diffs.size else 0.0
    spikes = [int(i + 1) for i, diff in enumerate(diffs) if diff > max(spike_threshold, 0)]
    recent = np.abs(diffs[-5:]) if diffs.size >= 5 else np.abs(diffs)
    plateau = bool(recent.size and np.all(recent < 1e-6))
    return {
        "num_points": int(len(ordered)),
        "missing_step_gaps": missing_steps,
        "spike_indices": spikes,
        "plateau_detected": plateau,
        "loss_start": float(losses[0]) if losses.size else None,
        "loss_end": float(losses[-1]) if losses.size else None,
        "caveat": "These are heuristic diagnostics and must be checked against the intended schedule.",
    }


def convergence_diagnostics(values: Sequence[float]) -> dict[str, object]:
    '''Summarize the trajectory of a numeric metric over ordered steps.'''
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        raise ValueError("at least one value is required")
    delta = float(arr[-1] - arr[0]) if arr.size > 1 else 0.0
    last_window = arr[-min(5, arr.size):]
    nondecreasing = bool(np.all(np.diff(arr) >= 0)) if arr.size > 1 else True
    return {
        "count": int(arr.size),
        "start": float(arr[0]),
        "end": float(arr[-1]),
        "delta": delta,
        "last_window_mean": float(last_window.mean()),
        "last_window_std": float(last_window.std(ddof=1)) if last_window.size > 1 else 0.0,
        "monotone_nonincreasing": bool(np.all(np.diff(arr) <= 0)) if arr.size > 1 else True,
        "monotone_nondecreasing": nondecreasing,
        "monotone_nondecresing": nondecreasing,
    }


def gradient_norm_summary(values: Sequence[float]) -> dict[str, object]:
    '''Summarize gradient norm values with documented heuristic flags.'''
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        raise ValueError("at least one value is required")
    flags: list[str] = []
    if np.max(arr) > 1e3:
        flags.append("explosion-like range: max norm exceeds 1e3")
    if np.median(arr) < 1e-8:
        flags.append("vanishing-like range: median norm below 1e-8")
    return {
        "count": int(arr.size),
        "mean": float(arr.mean()),
        "median": float(np.median(arr)),
        "min": float(arr.min()),
        "max": float(arr.max()),
        "flags": flags,
        "heuristic_thresholds": {"explosion_max_gt": 1e3, "vanishing_median_lt": 1e-8},
    }


def local_sensitivity(frame: pd.DataFrame, parameter_col: str, value_col: str) -> dict[str, object]:
    '''Compute finite local sensitivities for ordered numeric parameter values.'''
    if parameter_col not in frame or value_col not in frame:
        raise ValueError("parameter and value columns must exist")
    ordered = frame[[parameter_col, value_col]].sort_values(parameter_col)
    x = ordered[parameter_col].to_numpy(dtype=float)
    y = ordered[value_col].to_numpy(dtype=float)
    dx = np.diff(x)
    dy = np.diff(y)
    valid = dx != 0
    sensitivities = dy[valid] / dx[valid]
    return {
        "num_intervals": int(sensitivities.size),
        "sensitivities": sensitivities.tolist(),
        "mean_abs_sensitivity": float(np.mean(np.abs(sensitivities))) if sensitivities.size else 0.0,
        "max_abs_sensitivity": float(np.max(np.abs(sensitivities))) if sensitivities.size else 0.0,
    }
