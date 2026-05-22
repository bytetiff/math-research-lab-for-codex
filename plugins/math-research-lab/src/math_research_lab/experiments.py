from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd

from .cli_utils import flatten_dict


def check_split_overlap(frames: dict[str, pd.DataFrame], key_column: str) -> dict[str, Any]:
    '''Report exact key overlaps across named split data frames.'''
    keys: dict[str, set[str]] = {}
    for name, frame in frames.items():
        if key_column not in frame:
            raise ValueError(f"Missing key column {key_column} in split {name}")
        keys[name] = {str(v) for v in frame[key_column].dropna().tolist()}
    overlaps: list[dict[str, Any]] = []
    names = sorted(keys)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            common = sorted(keys[a].intersection(keys[b]))
            overlaps.append({"split_a": a, "split_b": b, "count": len(common), "overlap_keys": common})
    return {"key_column": key_column, "overlaps": overlaps}


def sha1_file(path: str | Path) -> str:
    '''Compute a SHA-1 digest for a file.'''
    digest = hashlib.sha1()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_duplicates(paths: list[str | Path]) -> dict[str, Any]:
    '''Hash files and report exact duplicate content groups.'''
    digest_to_paths: dict[str, list[str]] = {}
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            file_paths = sorted(p for p in path.rglob("*") if p.is_file())
        else:
            file_paths = [path]
        for file_path in file_paths:
            digest_to_paths.setdefault(sha1_file(file_path), []).append(str(file_path))
    duplicates = [
        {"sha1": digest, "paths": group, "count": len(group)}
        for digest, group in sorted(digest_to_paths.items()) if len(group) > 1
    ]
    return {"num_files_hashed": sum(len(group) for group in digest_to_paths.values()), "duplicates": duplicates}


def _load_config(path: str | Path) -> Any:
    path = Path(path)
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix == ".json":
        return json.loads(text)
    if suffix in {".yaml", ".yml"}:
        try:
            import yaml
        except ImportError as exc:
            raise RuntimeError("PyYAML is required to read YAML configs") from exc
        return yaml.safe_load(text)
    if suffix == ".toml":
        import tomllib
        return tomllib.loads(text)
    raise ValueError(f"Unsupported config format: {suffix}")


def config_diff(path_a: str | Path, path_b: str | Path) -> dict[str, Any]:
    '''Flatten and compare two JSON/YAML/TOML configuration files.'''
    a = flatten_dict(_load_config(path_a))
    b = flatten_dict(_load_config(path_b))
    all_keys = sorted(set(a).union(b))
    diffs = [
        {"key": key, "left": a.get(key), "right": b.get(key)}
        for key in all_keys if a.get(key) != b.get(key)
    ]
    return {"left": str(path_a), "right": str(path_b), "differences": diffs, "num_differences": len(diffs)}


def result_reproducibility_check(frame: pd.DataFrame, run_col: str = "run_id", seed_col: str = "seed", metric_col: str = "metric") -> dict[str, Any]:
    '''Summarize run/seed coverage and metric reproducibility.'''
    for column in [run_col, seed_col, metric_col]:
        if column not in frame:
            raise ValueError(f"Missing required column: {column}")
    metric = pd.to_numeric(frame[metric_col], errors="raise")
    seed_counts = frame.groupby(seed_col)[run_col].nunique().to_dict()
    warning = "Only one unique seed; replication stability cannot be assessed." if frame[seed_col].nunique() < 2 else None
    return {
        "num_runs": int(frame[run_col].nunique()),
        "num_rows": int(len(frame)),
        "num_unique_seeds": int(frame[seed_col].nunique()),
        "seed_counts": {str(k): int(v) for k, v in seed_counts.items()},
        "metric_mean": float(metric.mean()),
        "metric_std": float(metric.std(ddof=1)) if len(metric) > 1 else 0.0,
        "warnings": [warning] if warning else [],
    }
