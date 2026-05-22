from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def read_text_or_file(value: str) -> str:
    '''Read value as a path when it exists; otherwise return it as literal text.'''
    try:
        path = Path(value)
        if path.exists() and path.is_file():
            return path.read_text(encoding="utf-8")
    except OSError:
        pass
    return value


def load_json(path: str | Path) -> Any:
    '''Load JSON from a file with a clear error on invalid input.'''
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(data: Any) -> str:
    '''Serialize data as deterministic, readable JSON.'''
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)


def write_text_output(text: str, output: str | None = None) -> str:
    '''Write text to a file or print it; return the rendered text.'''
    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text(text, encoding="utf-8")
    else:
        print(text)
    return text


def write_json_output(data: Any, output: str | None = None) -> str:
    '''Write JSON to a file or print it; return the rendered JSON.'''
    return write_text_output(dump_json(data), output)


def read_csv_checked(path: str | Path, required_columns: list[str] | None = None) -> pd.DataFrame:
    '''Read a CSV file and validate required columns.'''
    df = pd.read_csv(path)
    missing = [col for col in (required_columns or []) if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(missing)}")
    return df


def flatten_dict(value: Any, prefix: str = "") -> dict[str, Any]:
    '''Flatten nested dict/list values into dotted paths for config comparison.'''
    flat: dict[str, Any] = {}
    if isinstance(value, dict):
        for key, item in value.items():
            nested = f"{prefix}.{key}" if prefix else str(key)
            flat.update(flatten_dict(item, nested))
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            nested = f"{prefix}[{idx}]"
            flat.update(flatten_dict(item, nested))
    else:
        flat[prefix] = value
    return flat
