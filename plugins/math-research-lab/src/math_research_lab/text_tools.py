from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

CLAIM_MARKERS = [
    "therefore", "implies", "shows", "proves", "suggests", "caused by",
    "because", "explains", "correlates", "improves", "outperforms", "indicates",
    "evidence", "mechanism", "demonstrates", "supports", "leads to",
]

ASSUMPTION_MARKERS = ["assume", "assuming", "suppose", "given", "under", "requires", "provided that", "if "]


def split_sentences(text: str) -> list[str]:
    '''Split prose into coarse sentence-like units.'''
    chunks = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def classify_claim(sentence: str) -> str:
    '''Heuristically classify a candidate research claim.'''
    s = sentence.lower()
    if any(word in s for word in ["caused", "because", "explains", "mechanism", "mediates"]):
        return "mechanistic"
    if any(word in s for word in ["prove", "theorem", "lemma", "converges", "implies", "therefore"]):
        return "theoretical"
    if any(word in s for word in ["metric", "accuracy", "loss", "score", "improves", "outperforms"]):
        return "metric"
    if any(word in s for word in ["implementation", "code", "kernel", "checkpoint", "configuration"]):
        return "implementation"
    if any(word in s for word in ["may", "might", "suggests", "plausible", "candidate"]):
        return "speculative"
    return "empirical"


def extract_claims(text: str) -> list[dict[str, Any]]:
    '''Extract candidate claims using explicit marker heuristics.'''
    claims: list[dict[str, Any]] = []
    for index, sentence in enumerate(split_sentences(text), start=1):
        lowered = sentence.lower()
        markers = [marker for marker in CLAIM_MARKERS if marker in lowered]
        if markers:
            claims.append({
                "id": f"C{len(claims) + 1}",
                "sentence_index": index,
                "text": sentence,
                "markers": markers,
                "heuristic_type": classify_claim(sentence),
                "classification_note": "Heuristic marker-based classification; verify manually before using as evidence.",
            })
    return claims


def extract_math_objects(text: str) -> dict[str, Any]:
    '''Extract likely symbols and formula fragments without claiming full LaTeX parsing.'''
    formula_patterns = [r"\$([^$]+)\$", r"\\\((.*?)\\\)", r"\\\[(.*?)\\\]"]
    formulas: list[str] = []
    for pattern in formula_patterns:
        formulas.extend(match.strip() for match in re.findall(pattern, text, flags=re.DOTALL))
    symbol_pattern = re.compile(r"(?<![A-Za-z])(?:[A-Za-z](?:_[A-Za-z0-9]+|\^[A-Za-z0-9]+)?|\\[a-zA-Z]+)(?![A-Za-z])")
    symbols = sorted(set(symbol_pattern.findall(text)))
    return {
        "symbols": symbols,
        "formula_fragments": formulas,
        "note": "Regex heuristic only; this does not parse arbitrary LaTeX or infer semantic roles.",
    }


def build_assumption_table(text: str) -> str:
    '''Render explicit and possible hidden assumptions as a markdown table.'''
    rows: list[tuple[str, str, str]] = []
    for sentence in split_sentences(text):
        lower = sentence.lower()
        if any(marker in lower for marker in ASSUMPTION_MARKERS):
            rows.append(("explicit", sentence, "Detected from assumption marker; confirm scope."))
    hidden = suggest_hidden_assumptions(text)
    for item in hidden:
        rows.append(("possible hidden", item, "Suggestion from common mathematical precondition; not a fact."))
    if not rows:
        rows.append(("none detected", "No explicit assumption marker detected", "Manual review still required."))
    lines = ["| Kind | Assumption | Note |", "|---|---|---|"]
    lines.extend(f"| {kind} | {assumption} | {note} |" for kind, assumption, note in rows)
    return "\n".join(lines)


def suggest_hidden_assumptions(text: str) -> list[str]:
    '''Suggest common hidden assumptions based on terms in text.'''
    lower = text.lower()
    suggestions: list[str] = []
    if "divide" in lower or "/" in text:
        suggestions.append("Denominators are nonzero on the claimed domain.")
    if "inverse" in lower or "invert" in lower:
        suggestions.append("The relevant matrix, map, or operator is invertible where used.")
    if "gradient" in lower or "derivative" in lower:
        suggestions.append("Differentiability and numerical smoothness hold in the region tested.")
    if "expectation" in lower or "mean" in lower:
        suggestions.append("The sample or distribution supports the stated expectation or mean estimate.")
    if "argmax" in lower or "maximum" in lower:
        suggestions.append("Tie-breaking and boundary cases are defined.")
    return suggestions


def check_symbol_reuse(text: str) -> list[dict[str, Any]]:
    '''Identify symbols that appear in multiple contexts or lines.'''
    objects = extract_math_objects(text)["symbols"]
    locations: dict[str, list[int]] = defaultdict(list)
    lines = text.splitlines() or [text]
    for line_number, line in enumerate(lines, start=1):
        for symbol in objects:
            if re.search(rf"(?<![A-Za-z]){re.escape(symbol)}(?![A-Za-z])", line):
                locations[symbol].append(line_number)
    return [
        {"symbol": symbol, "locations": locs, "risk": "review for reuse or role changes"}
        for symbol, locs in sorted(locations.items()) if len(locs) > 1
    ]


def build_notation_table(symbols: list[str] | list[dict[str, Any]]) -> str:
    '''Render a notation table from symbols or metadata dictionaries.'''
    lines = ["| Symbol | Meaning | Domain/Codomain | Dimension | Status |", "|---|---|---|---|---|"]
    for item in symbols:
        if isinstance(item, dict):
            symbol = item.get("symbol", "")
            meaning = item.get("meaning", "")
            domain = item.get("domain", item.get("codomain", ""))
            dimension = item.get("dimension", "")
            status = item.get("status", "needs definition")
        else:
            symbol, meaning, domain, dimension, status = item, "", "", "", "needs definition"
        lines.append(f"| {symbol} | {meaning} | {domain} | {dimension} | {status} |")
    return "\n".join(lines)


def dimension_table(symbol_metadata: list[dict[str, Any]]) -> str:
    '''Render a domain/codomain/dimension table from JSON symbol metadata.'''
    lines = ["| Symbol | Domain | Codomain | Dimension | Unit | Notes |", "|---|---|---|---|---|---|"]
    for item in symbol_metadata:
        lines.append(
            f"| {item.get('symbol', '')} | {item.get('domain', '')} | {item.get('codomain', '')} | "
            f"{item.get('dimension', '')} | {item.get('unit', '')} | {item.get('notes', '')} |"
        )
    return "\n".join(lines)


def implication_checklist(argument_text: str) -> str:
    '''Create a manual implication checklist from a proof or argument.'''
    sentences = split_sentences(argument_text)
    lines = ["| Step | Statement | Review Status | Required Assumptions | Notes |", "|---:|---|---|---|---|"]
    for index, sentence in enumerate(sentences, start=1):
        lines.append(f"| {index} | {sentence} | unchecked |  |  |")
    if not sentences:
        lines.append("| 1 | No implication text supplied | unchecked |  |  |")
    return "\n".join(lines)


def terminology_risks(text: str) -> list[dict[str, str]]:
    '''Find risky overclaiming phrases and cautious alternatives.'''
    replacements = {
        "proves": "supports under the stated assumptions",
        "new principle": "candidate framing requiring literature validation",
        "caused by": "is consistent with, pending causal isolation",
        "general law": "observed pattern within the tested scope",
        "novel mechanism": "candidate mechanism requiring direct measurement and literature validation",
        "demonstrates conclusively": "provides evidence for",
    }
    lower = text.lower()
    return [
        {"phrase": phrase, "suggested_cautious_wording": replacement}
        for phrase, replacement in replacements.items() if phrase in lower
    ]


def forbidden_wording_occurrences(text: str, forbidden: list[str]) -> list[dict[str, Any]]:
    '''Report occurrences of forbidden phrases without rewriting automatically.'''
    results: list[dict[str, Any]] = []
    lower = text.lower()
    for phrase in forbidden:
        start = 0
        phrase_lower = phrase.lower()
        while True:
            idx = lower.find(phrase_lower, start)
            if idx == -1:
                break
            results.append({"phrase": phrase, "index": idx, "suggestion": "Replace with evidence-bounded wording."})
            start = idx + len(phrase_lower)
    return results
