from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from .safe_expr import evaluate_expression


def audit_metric_matrix(
    frame: pd.DataFrame,
    row_col: str = "row",
    col_col: str = "col",
    value_col: str = "value",
) -> dict[str, Any]:
    '''Audit a generic matrix-shaped metric input table.'''
    for column in [row_col, col_col, value_col]:
        if column not in frame.columns:
            raise ValueError(f"Missing required column: {column}")
    duplicates_frame = frame[frame.duplicated([row_col, col_col], keep=False)].sort_values([row_col, col_col])
    duplicate_cells = [
        {
            "row": row,
            "col": col,
            "values": group[value_col].tolist(),
            "count": int(len(group)),
        }
        for (row, col), group in duplicates_frame.groupby([row_col, col_col], sort=True)
    ]
    deduped = frame.groupby([row_col, col_col], as_index=False)[value_col].mean()
    pivot = deduped.pivot(index=row_col, columns=col_col, values=value_col).sort_index().sort_index(axis=1)
    row_values = list(pivot.index)
    col_values = list(pivot.columns)
    index_union = sorted(set(row_values).union(set(col_values)))
    missing_diagonal = [idx for idx in index_union if idx not in pivot.index or idx not in pivot.columns or pd.isna(pivot.loc[idx, idx])]
    final_row = row_values[-1] if row_values else None
    final_row_missing_cols: list[Any] = []
    if final_row is not None:
        final_row_missing_cols = [col for col in col_values if pd.isna(pivot.loc[final_row, col])]
    return {
        "shape": [int(pivot.shape[0]), int(pivot.shape[1])],
        "rows": row_values,
        "cols": col_values,
        "duplicate_cells": duplicate_cells,
        "missing_diagonal": missing_diagonal,
        "final_row": final_row,
        "final_row_missing_cols": final_row_missing_cols,
        "inconsistent_index_ranges": row_values != col_values,
        "pivot_table": pivot.where(pd.notna(pivot), None).to_dict(),
        "interpretation_boundary": "This audits matrix construction and aggregation; it does not establish a mechanism.",
    }


def recompute_metric_from_aggregates(frame: pd.DataFrame, expression: str) -> dict[str, Any]:
    '''Evaluate a restricted expression over aggregate numeric columns.'''
    numeric = frame.select_dtypes(include=[np.number])
    if numeric.empty:
        raise ValueError("no numeric columns available for aggregate expression")
    variables: dict[str, float] = {}
    for column in numeric.columns:
        values = numeric[column].dropna()
        variables[f"mean_{column}"] = float(values.mean())
        variables[f"sum_{column}"] = float(values.sum())
        variables[f"min_{column}"] = float(values.min())
        variables[f"max_{column}"] = float(values.max())
        variables[f"count_{column}"] = float(values.count())
    value = evaluate_expression(expression, variables)
    return {
        "expression": expression,
        "value": float(value) if isinstance(value, (int, float, np.floating)) else value,
        "available_variables": sorted(variables),
        "note": "Expression evaluated with a restricted parser over aggregate columns only.",
    }


def decompose_metric_contributions(frame: pd.DataFrame, item_col: str, contribution_col: str) -> dict[str, Any]:
    '''Sort positive and negative contribution terms and summarize them.'''
    if item_col not in frame or contribution_col not in frame:
        raise ValueError("item and contribution columns must exist")
    contributions = frame[[item_col, contribution_col]].copy()
    contributions[contribution_col] = pd.to_numeric(contributions[contribution_col], errors="raise")
    total = float(contributions[contribution_col].sum())
    sorted_rows = contributions.sort_values(contribution_col)
    negative = sorted_rows[sorted_rows[contribution_col] < 0]
    positive = sorted_rows[sorted_rows[contribution_col] > 0].sort_values(contribution_col, ascending=False)
    return {
        "total_contribution": total,
        "num_items": int(len(contributions)),
        "positive_contributors": positive.to_dict(orient="records"),
        "negative_contributors": negative.to_dict(orient="records"),
        "summary": {
            "mean": float(contributions[contribution_col].mean()),
            "std": float(contributions[contribution_col].std(ddof=1)) if len(contributions) > 1 else 0.0,
            "min": float(contributions[contribution_col].min()),
            "max": float(contributions[contribution_col].max()),
        },
        "interpretation_boundary": "Contribution terms are algebraic or accounting components unless separately tied to a mechanism.",
    }


def compare_metric_definitions(definitions: list[dict[str, Any]]) -> str:
    '''Render a markdown report comparing alternative metric definitions.'''
    lines = ["# Metric Definition Comparison", "", "| Name | Value | Inputs | Aggregation | Caveat |", "|---|---:|---|---|---|"]
    for item in definitions:
        lines.append(
            f"| {item.get('name', '')} | {item.get('value', '')} | {item.get('inputs', '')} | "
            f"{item.get('aggregation', '')} | {item.get('caveat', '')} |"
        )
    lines.extend([
        "",
        "Alternative definitions are not interchangeable. Treat discrepancies as scope or convention differences until justified.",
    ])
    return "\n".join(lines)
