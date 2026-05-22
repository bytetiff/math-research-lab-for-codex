from __future__ import annotations

from typing import Any, Sequence

import numpy as np


def singular_values_from_input(matrix_or_values: np.ndarray | Sequence[float], values_are_singular: bool = False) -> np.ndarray:
    '''Return nonnegative singular values from a matrix or provided values.'''
    arr = np.asarray(matrix_or_values, dtype=float)
    if values_are_singular:
        values = np.abs(arr.ravel())
    else:
        if arr.ndim != 2:
            raise ValueError("matrix input must be 2D")
        values = np.linalg.svd(arr, compute_uv=False)
    return values


def svd_energy(matrix: np.ndarray, rank: int | None = None) -> dict[str, Any]:
    '''Compute singular values and retained squared-energy share.'''
    s = singular_values_from_input(matrix)
    if rank is None:
        rank = int(len(s))
    if rank < 0:
        raise ValueError("rank must be nonnegative")
    total = float(np.sum(s ** 2))
    cumulative = np.cumsum(s ** 2) / total if total > 0 else np.zeros_like(s)
    retained = float(cumulative[min(rank, len(s)) - 1]) if total > 0 and rank > 0 and len(s) else 0.0
    return {
        "singular_values": s.tolist(),
        "cumulative_energy": cumulative.tolist(),
        "rank": int(rank),
        "retained_energy": retained,
    }


def spectral_entropy(values: np.ndarray | Sequence[float], values_are_singular: bool = True) -> dict[str, Any]:
    '''Compute normalized entropy of squared singular/eigenvalue energy.'''
    s = singular_values_from_input(values, values_are_singular=values_are_singular)
    energy = s ** 2
    total = float(energy.sum())
    if total <= 0 or s.size == 0:
        entropy = 0.0
        normalized = 0.0
    else:
        p = energy / total
        p = p[p > 0]
        entropy = float(-np.sum(p * np.log(p)))
        normalized = float(entropy / np.log(len(s))) if len(s) > 1 else 0.0
    return {"spectral_entropy": entropy, "normalized_spectral_entropy": normalized, "num_components": int(s.size)}


def effective_rank(values: np.ndarray | Sequence[float], values_are_singular: bool = True) -> dict[str, Any]:
    '''Compute entropy-based effective rank.'''
    entropy = spectral_entropy(values, values_are_singular=values_are_singular)["spectral_entropy"]
    return {"effective_rank": float(np.exp(entropy)), "spectral_entropy": float(entropy)}


def low_rank_reconstruction(matrix: np.ndarray, rank: int) -> dict[str, Any]:
    '''Compute truncated-SVD reconstruction error for a matrix.'''
    x = np.asarray(matrix, dtype=float)
    if x.ndim != 2:
        raise ValueError("matrix must be 2D")
    if rank < 0:
        raise ValueError("rank must be nonnegative")
    u, s, vt = np.linalg.svd(x, full_matrices=False)
    r = min(rank, len(s))
    recon = (u[:, :r] * s[:r]) @ vt[:r, :] if r else np.zeros_like(x)
    fro = float(np.linalg.norm(x - recon, ord="fro"))
    denom = float(np.linalg.norm(x, ord="fro"))
    return {
        "rank": int(rank),
        "used_rank": int(r),
        "frobenius_error": fro,
        "relative_frobenius_error": float(fro / denom) if denom else 0.0,
    }
