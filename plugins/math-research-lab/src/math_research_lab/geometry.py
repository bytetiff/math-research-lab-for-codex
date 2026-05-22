from __future__ import annotations

from typing import Any, Sequence

import numpy as np


def _summary(values: np.ndarray) -> dict[str, float | int]:
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        return {"count": 0, "mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0, "median": 0.0}
    return {
        "count": int(arr.size),
        "mean": float(arr.mean()),
        "std": float(arr.std(ddof=1)) if arr.size > 1 else 0.0,
        "min": float(arr.min()),
        "max": float(arr.max()),
        "median": float(np.median(arr)),
    }


def pairwise_distance_summary(features: np.ndarray) -> dict[str, Any]:
    '''Compute summary statistics for Euclidean pairwise distances.'''
    x = np.asarray(features, dtype=float)
    if x.ndim != 2:
        raise ValueError("features must be a 2D array")
    if x.shape[0] < 2:
        distances = np.array([], dtype=float)
    else:
        diffs = x[:, None, :] - x[None, :, :]
        full = np.sqrt(np.sum(diffs * diffs, axis=2))
        distances = full[np.triu_indices(x.shape[0], k=1)]
    result = _summary(distances)
    result["num_vectors"] = int(x.shape[0])
    result["dimension"] = int(x.shape[1])
    return result


def prototype_geometry(features: np.ndarray, labels: Sequence[object]) -> dict[str, Any]:
    '''Compute class prototypes, inter-prototype distances, and intra-class variance.'''
    x = np.asarray(features, dtype=float)
    y = np.asarray(labels)
    if x.ndim != 2:
        raise ValueError("features must be a 2D array")
    if y.shape[0] != x.shape[0]:
        raise ValueError("labels length must match number of feature rows")
    prototypes: dict[str, np.ndarray] = {}
    intra: dict[str, float] = {}
    for label in sorted({str(v) for v in y}):
        class_features = x[y.astype(str) == label]
        proto = class_features.mean(axis=0)
        prototypes[label] = proto
        intra[label] = float(np.mean(np.sum((class_features - proto) ** 2, axis=1)))
    proto_labels = list(prototypes)
    distances: list[dict[str, object]] = []
    for i, a in enumerate(proto_labels):
        for b in proto_labels[i + 1:]:
            distances.append({"label_a": a, "label_b": b, "distance": float(np.linalg.norm(prototypes[a] - prototypes[b]))})
    return {
        "prototypes": {label: value.tolist() for label, value in prototypes.items()},
        "inter_prototype_distances": distances,
        "intra_class_variance": intra,
        "note": "Prototype geometry is descriptive unless tied to a tested target metric or mechanism.",
    }


def margins(logits: np.ndarray, labels: Sequence[int]) -> np.ndarray:
    '''Compute true-logit minus best-other-logit margins.'''
    z = np.asarray(logits, dtype=float)
    y = np.asarray(labels, dtype=int)
    if z.ndim != 2:
        raise ValueError("logits must be a 2D array")
    if y.shape[0] != z.shape[0]:
        raise ValueError("labels length must match logits rows")
    if np.any(y < 0) or np.any(y >= z.shape[1]):
        raise ValueError("labels must be valid class indices")
    true = z[np.arange(z.shape[0]), y]
    masked = z.copy()
    masked[np.arange(z.shape[0]), y] = -np.inf
    best_other = np.max(masked, axis=1)
    return true - best_other


def margin_analysis(logits: np.ndarray, labels: Sequence[int], before_logits: np.ndarray | None = None) -> dict[str, Any]:
    '''Summarize margins and optional before/after boundary crossings.'''
    after = np.asarray(logits, dtype=float)
    y = np.asarray(labels, dtype=int)
    after_margins = margins(after, y)
    result: dict[str, Any] = {
        "margin_definition": "true_logit - max_other_logit",
        "overall": _summary(after_margins),
        "per_class": {},
    }
    for label in sorted(set(y.tolist())):
        result["per_class"][str(label)] = _summary(after_margins[y == label])
    if before_logits is not None:
        before = np.asarray(before_logits, dtype=float)
        if before.shape != after.shape:
            raise ValueError("before_logits must match logits shape")
        before_margins = margins(before, y)
        gain = after_margins - before_margins
        before_pred = before.argmax(axis=1)
        after_pred = after.argmax(axis=1)
        result["before_after"] = {
            "mean_margin_gain": float(gain.mean()),
            "median_margin_gain": float(np.median(gain)),
            "negative_to_positive_crossing_rate": float(np.mean((before_margins < 0) & (after_margins >= 0))),
            "positive_to_negative_crossing_rate": float(np.mean((before_margins >= 0) & (after_margins < 0))),
            "num_prediction_flips": int(np.sum(before_pred != after_pred)),
        }
    result["caveat"] = "Margins describe classifier geometry; they do not prove a causal mechanism by themselves."
    return result


def embedding_drift(before: np.ndarray, after: np.ndarray) -> dict[str, Any]:
    '''Summarize row-wise embedding drift norms.'''
    a = np.asarray(before, dtype=float)
    b = np.asarray(after, dtype=float)
    if a.shape != b.shape:
        raise ValueError("before and after arrays must have the same shape")
    norms = np.linalg.norm(b - a, axis=1)
    result = _summary(norms)
    result["num_vectors"] = int(a.shape[0])
    result["dimension"] = int(a.shape[1]) if a.ndim == 2 else 0
    return result
