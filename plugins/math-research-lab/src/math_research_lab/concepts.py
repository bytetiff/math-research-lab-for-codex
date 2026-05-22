from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def slugify(name: str) -> str:
    '''Create a filesystem-safe concept slug.'''
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower()).strip("-")
    if not slug:
        raise ValueError("concept name must contain at least one alphanumeric character")
    return slug


def pattern_discovery(frame: pd.DataFrame) -> dict[str, Any]:
    '''Compute exploratory numeric correlations and outlier summaries.'''
    numeric = frame.select_dtypes(include=[np.number])
    if numeric.empty:
        raise ValueError("pattern discovery requires numeric columns")
    corr = numeric.corr(method="pearson").fillna(0.0)
    outliers: dict[str, list[int]] = {}
    for column in numeric.columns:
        values = numeric[column]
        std = values.std(ddof=1)
        if std and not np.isnan(std):
            z = (values - values.mean()) / std
            outliers[column] = [int(i) for i in values.index[np.abs(z) > 3].tolist()]
        else:
            outliers[column] = []
    return {
        "correlations": corr.to_dict(),
        "outlier_indices_by_column": outliers,
        "note": "Exploratory pattern discovery only; it does not establish causation or novelty.",
    }


def hypothesis_graph(case: dict[str, Any]) -> str:
    '''Render a markdown evidence graph/table from structured hypotheses.'''
    lines = ["# Hypothesis Evidence Graph", "", "| Hypothesis | Supports | Missing | Contradicts | Related To |", "|---|---|---|---|---|"]
    for item in case.get("hypotheses", []):
        lines.append(
            f"| {item.get('name', '')} | {', '.join(item.get('supporting_evidence', []))} | "
            f"{', '.join(item.get('missing_evidence', []))} | {', '.join(item.get('contradictory_evidence', []))} | "
            f"{', '.join(item.get('relationships', []))} |"
        )
    return "\n".join(lines)


def concept_report(concept: dict[str, Any]) -> str:
    '''Render a cautious candidate concept report.'''
    lines = [
        f"# Candidate Concept: {concept.get('name', 'unnamed')}",
        "",
        f"Status: {concept.get('status', 'unsupported speculation')}",
        "",
        "## Operational Definition",
        str(concept.get("operational_definition", "Not supplied.")),
        "",
        "## Observed Pattern",
        str(concept.get("observed_pattern", "Not supplied.")),
        "",
        "## Evidence Needed",
    ]
    evidence_needed = concept.get("evidence_needed", []) or ["Direct measurements, alternatives, and literature validation as applicable."]
    lines.extend(f"- {item}" for item in evidence_needed)
    lines.extend(["", "This report does not claim novelty."])
    return "\n".join(lines)


def concept_overlap_table(case: dict[str, Any]) -> str:
    '''Render a concept overlap comparison table.'''
    candidate = case.get("candidate", {})
    lines = [f"# Concept Overlap: {candidate.get('name', 'candidate')}", "", "| Nearby Concept | Shared Structure | Difference | Risk |", "|---|---|---|---|"]
    for item in case.get("nearby_concepts", []):
        lines.append(
            f"| {item.get('name', '')} | {item.get('shared_structure', '')} | "
            f"{item.get('difference', '')} | {item.get('risk', '')} |"
        )
    return "\n".join(lines)


def render_concept_record(concept: dict[str, Any]) -> str:
    '''Render a concept registry markdown record.'''
    today = concept.get("date", date.today().isoformat())
    evidence = concept.get("evidence_table", [])
    lines = [
        f"# {concept['name']}",
        "",
        f"Status: {concept.get('status', 'unsupported speculation')}",
        f"Date created/updated: {today}",
        "",
        "## Operational Definition",
        str(concept.get("operational_definition", "")),
        "",
        "## Observed Pattern",
        str(concept.get("observed_pattern", "")),
        "",
        "## Evidence Table",
        "| Evidence | Type | Direction | Level | Note |",
        "|---|---|---|---:|---|",
    ]
    if evidence:
        for item in evidence:
            lines.append(f"| {item.get('evidence', '')} | {item.get('type', '')} | {item.get('direction', '')} | {item.get('level', '')} | {item.get('note', '')} |")
    else:
        lines.append("| None supplied | missing | missing | 0 | Add evidence before strengthening the concept. |")
    sections = [
        ("Evidence Level", concept.get("evidence_level", "0")),
        ("Nearby Concepts", concept.get("nearby_concepts", [])),
        ("Distinction From Nearby Concepts", concept.get("distinction_from_nearby_concepts", "")),
        ("Falsification Tests", concept.get("falsification_tests", [])),
        ("Contradictory Evidence", concept.get("contradictory_evidence", [])),
        ("Missing Evidence", concept.get("missing_evidence", [])),
        ("Forbidden Wording", concept.get("forbidden_wording", [])),
        ("Safe Wording", concept.get("safe_wording", "")),
        ("Next Decisive Experiments", concept.get("next_decisive_experiments", [])),
        ("Judge Verdict", concept.get("judge_verdict", "not fully evaluated")),
    ]
    for title, value in sections:
        lines.extend(["", f"## {title}"])
        if isinstance(value, list):
            lines.extend(f"- {item}" for item in (value or ["None supplied."]))
        else:
            lines.append(str(value))
    lines.extend(["", "## History", f"- {today}: Record created or updated."])
    return "\n".join(lines)


def create_concept_record(concept: dict[str, Any], root: str | Path = ".") -> Path:
    '''Create a concept record under research_notes/concept_registry.'''
    if "name" not in concept:
        raise ValueError("concept JSON must include a name")
    registry = Path(root) / "research_notes" / "concept_registry"
    registry.mkdir(parents=True, exist_ok=True)
    path = registry / f"{slugify(concept['name'])}.md"
    if path.exists():
        raise FileExistsError(f"concept record already exists: {path}")
    path.write_text(render_concept_record(concept), encoding="utf-8")
    return path


def update_evidence_table(path: str | Path, evidence_items: list[dict[str, Any]]) -> Path:
    '''Append evidence updates to an existing concept record while preserving history.'''
    record = Path(path)
    if not record.exists():
        raise FileNotFoundError(record)
    today = date.today().isoformat()
    lines = ["", f"## Evidence Update {today}", "| Evidence | Type | Direction | Level | Note |", "|---|---|---|---:|---|"]
    for item in evidence_items:
        lines.append(f"| {item.get('evidence', '')} | {item.get('type', '')} | {item.get('direction', '')} | {item.get('level', '')} | {item.get('note', '')} |")
    lines.extend(["", f"- {today}: Evidence table updated; previous entries preserved."])
    with record.open("a", encoding="utf-8") as handle:
        handle.write("\n" + "\n".join(lines) + "\n")
    return record


def concept_status_check(status: str, evidence_level: int, literature_validated: bool = False) -> dict[str, Any]:
    '''Validate concept status against evidence level and literature-review state.'''
    normalized = status.strip().lower()
    errors: list[str] = []
    warnings: list[str] = []
    if normalized in {"novel", "confirmed novel", "new concept"} and not literature_validated:
        errors.append("Novelty status requires explicit literature validation.")
    if "mechanism" in normalized and evidence_level < 4:
        errors.append("Mechanism-level status requires direct mechanism evidence at level 4 or higher.")
    if evidence_level < 2 and normalized in {"supported", "known", "candidate new framing"}:
        warnings.append("Evidence level is low for a strengthened concept status.")
    if "potentially novel" in normalized and not literature_validated:
        warnings.append("Use only as an unverified candidate framing; do not claim novelty.")
    return {"status": status, "evidence_level": evidence_level, "literature_validated": literature_validated, "valid": not errors, "errors": errors, "warnings": warnings}
