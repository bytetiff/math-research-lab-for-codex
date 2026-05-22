from __future__ import annotations

from typing import Any

EVIDENCE_LEVELS = {
    0: "unsupported speculation",
    1: "plausible interpretation",
    2: "correlational evidence",
    3: "controlled ablation evidence",
    4: "mechanistic measurement",
    5: "replicated mechanism",
}

GENERIC_DOWNGRADE_REASONS = {
    "more experiments are needed",
    "this may not generalize",
    "the mechanism is not proven",
    "this may be an artifact",
    "this may already be known",
    "the evidence is insufficient",
    "the claim is too strong",
    "insufficient evidence",
}

VALID_VERDICTS = [
    "supported",
    "weakly supported",
    "diagnostic only",
    "promising but unproven",
    "likely artifact",
    "rejected",
    "not fully evaluated",
]


def _item_level(item: dict[str, Any]) -> int:
    if "level" in item:
        return int(item["level"])
    kind = str(item.get("type", item.get("kind", ""))).lower()
    if "replicated" in kind:
        return 5
    if "direct" in kind or "mechanistic" in kind or "measurement" in kind:
        return 4
    if "ablation" in kind or "intervention" in kind or "controlled" in kind:
        return 3
    if "correlation" in kind or "association" in kind or "metric" in kind:
        return 2
    if kind or item.get("description"):
        return 1
    return 0


def confidence_for_level(level: int, major_unresolved_alternative: bool = False) -> str:
    '''Map an evidence level to the required confidence label.'''
    if level <= 0:
        return "unsupported"
    if level in {1, 2}:
        return "low"
    if level == 3 or (level == 4 and major_unresolved_alternative):
        return "medium"
    return "high"


def score_research_claim(case: dict[str, Any]) -> dict[str, Any]:
    '''Score a research claim while separating missing from contradictory evidence.'''
    claim_type = str(case.get("claim_type", "empirical")).lower()
    evidence_items = case.get("evidence_items", []) or []
    missing = case.get("missing_evidence", []) or []
    contradictory = case.get("contradictory_evidence", []) or []
    artifact_risks = case.get("artifact_risks", []) or []
    literature_validated = bool(case.get("literature_validated", False))
    replications = int(case.get("replications", 0) or 0)
    levels = [_item_level(item) for item in evidence_items]
    level = max(levels) if levels else 0
    reasons: list[str] = []
    caps: list[str] = []
    direct_measurement = any(_item_level(item) >= 4 for item in evidence_items)
    controlled_ablation = any(_item_level(item) >= 3 for item in evidence_items)
    if replications > 1 and direct_measurement and not contradictory and not artifact_risks:
        level = max(level, 5)
        reasons.append("replicated direct evidence raises the possible evidence level")
    if "mechanism" in claim_type and not direct_measurement:
        if level > 3:
            level = 3
        caps.append("mechanism claim lacks direct mechanism measurement; confidence cannot be high")
    if "method" in claim_type and "causal" in claim_type and not controlled_ablation:
        if level > 2:
            level = 2
        caps.append("method-component causal claim lacks mechanism-isolating ablation")
    if "novel" in claim_type or "novelty" in claim_type:
        if not literature_validated:
            if level > 2:
                level = 2
            caps.append("novelty claim lacks literature validation")
        elif level < 5:
            caps.append("novelty claim requires level 5 evidence plus literature validation")
    if contradictory:
        if level > 2:
            level = 2
        reasons.append("contradictory evidence caps the claim until reconciled")
    if artifact_risks and level > 3:
        level = 3
        caps.append("concrete artifact risks remain unresolved")
    major_unresolved = bool(artifact_risks or contradictory or (missing and "mechanism" in claim_type))
    direction = {
        "supporting": len(evidence_items),
        "missing": len(missing),
        "contradictory": len(contradictory),
        "artifact-risk": len(artifact_risks),
    }
    if missing and not contradictory:
        reasons.append("missing evidence lowers or caps confidence but is not contradictory evidence")
    return {
        "claim": case.get("claim", ""),
        "claim_type": claim_type,
        "evidence_level": int(level),
        "evidence_level_label": EVIDENCE_LEVELS[int(level)],
        "confidence": confidence_for_level(int(level), major_unresolved),
        "evidence_direction_summary": direction,
        "reasons": reasons,
        "caps_applied": caps,
        "missing_is_not_contradictory": bool(missing and not contradictory),
    }


def compare_hypotheses(case: dict[str, Any]) -> dict[str, Any]:
    '''Rank hypotheses conservatively and preserve ties when evidence cannot discriminate.'''
    ranked: list[dict[str, Any]] = []
    for item in case.get("hypotheses", []):
        support = item.get("supporting_evidence", []) or []
        missing = item.get("missing_evidence", []) or []
        contradictory = item.get("contradictory_evidence", []) or []
        score = sum(_item_level(ev) if isinstance(ev, dict) else 1 for ev in support)
        score -= 2 * len(contradictory)
        score -= 0.25 * len(missing)
        ranked.append({**item, "score": float(score)})
    ranked.sort(key=lambda x: x["score"], reverse=True)
    tie = len(ranked) > 1 and abs(ranked[0]["score"] - ranked[1]["score"]) < 1e-9
    return {
        "ranked_hypotheses": ranked,
        "tie": tie,
        "winner": None if tie else (ranked[0].get("name") if ranked else None),
        "note": "No winner is selected when available evidence does not discriminate alternatives.",
    }


def rank_next_experiments(experiments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    '''Rank experiments by the required expected-information-gain heuristic.'''
    ranked: list[dict[str, Any]] = []
    for item in experiments:
        if not item.get("separates_hypotheses"):
            raise ValueError("each experiment must state which competing hypotheses it separates")
        score = (
            float(item.get("discrimination_power", 0))
            + float(item.get("falsification_power", 0))
            + float(item.get("mechanism_visibility", 0))
            - float(item.get("implementation_cost", 0))
            - float(item.get("implementation_risk", 0))
        )
        ranked.append({**item, "expected_information_gain_score": score})
    return sorted(ranked, key=lambda x: x["expected_information_gain_score"], reverse=True)


def validate_downgrade(item: dict[str, Any]) -> dict[str, Any]:
    '''Validate one proposed downgrade against the No Unsupported Downgrade Rule.'''
    required = [
        "original_claim",
        "downgraded_claim",
        "reason",
        "evidence_basis",
        "issue_type",
        "alternative_explanation",
        "decisive_test",
        "supported_evidence_preserved",
    ]
    missing = [key for key in required if not item.get(key)]
    reason = str(item.get("reason", "")).strip().lower().rstrip(".")
    generic = reason in GENERIC_DOWNGRADE_REASONS
    issue_ok = str(item.get("issue_type", "")).lower() in {"missing evidence", "contradictory evidence", "artifact-risk", "scope mismatch", "nearby known concept", "failed decisive test"}
    justified = not missing and not generic and issue_ok
    problems: list[str] = []
    if missing:
        problems.append("missing required field(s): " + ", ".join(missing))
    if generic:
        problems.append("generic skepticism is not a valid downgrade reason")
    if not issue_ok:
        problems.append("issue_type must be concrete and evidence-bound")
    return {**item, "justified": justified, "problems": problems}


def downgrade_ledger(items: list[dict[str, Any]]) -> dict[str, Any]:
    '''Validate proposed downgrades and return a ledger.'''
    rows = [validate_downgrade(item) for item in items]
    return {"downgrades": rows, "all_justified": all(row["justified"] for row in rows)}


def render_downgrade_ledger(items: list[dict[str, Any]]) -> str:
    '''Render the downgrade ledger as markdown.'''
    rows = downgrade_ledger(items)["downgrades"]
    lines = ["| Original Claim | Downgraded Claim | Reason | Evidence Basis | Missing or Contradictory? | Alternative Explanation | Decisive Test | Justified? |", "|---|---|---|---|---|---|---|---|"]
    for row in rows:
        lines.append(
            f"| {row.get('original_claim', '')} | {row.get('downgraded_claim', '')} | {row.get('reason', '')} | "
            f"{row.get('evidence_basis', '')} | {row.get('issue_type', '')} | {row.get('alternative_explanation', '')} | "
            f"{row.get('decisive_test', '')} | {row.get('justified')} |"
        )
    return "\n".join(lines)


def arbiter_check(case: dict[str, Any]) -> dict[str, Any]:
    '''Separate valid objections from unsupported objections while preserving proponent evidence.'''
    downgrades = [validate_downgrade(item) for item in case.get("proposed_downgrades", [])]
    valid = [item for item in downgrades if item["justified"]]
    unsupported = [item for item in downgrades if not item["justified"]]
    preserved = case.get("evidence_that_must_be_preserved", []) or []
    critique = case.get("judge_critique", "")
    critique_text = " ".join(map(str, critique)) if isinstance(critique, list) else str(critique)
    evidence_ignored = [ev for ev in preserved if str(ev) not in critique_text]
    if unsupported and not valid:
        verdict = "not fully evaluated"
    elif valid:
        verdict = "weakly supported"
    else:
        verdict = "supported"
    final_wording = case.get("final_justified_wording") or case.get("central_claim", "")
    return {
        "valid_objections": valid,
        "unsupported_objections": unsupported,
        "preserved_evidence": preserved,
        "evidence_ignored_by_judge": evidence_ignored,
        "final_justified_wording": final_wording,
        "recommended_verdict": verdict,
    }


def build_critique_report(case: dict[str, Any]) -> str:
    '''Build a research judge report using the required fixed section structure.'''
    claim = case.get("central_claim", case.get("claim", ""))
    score = score_research_claim(case)
    alternatives = case.get("alternative_hypotheses", [])
    downgrades = case.get("proposed_downgrades", [])
    arbiter = arbiter_check({
        "central_claim": claim,
        "proponent_case": case.get("proponent_case", []),
        "judge_critique": case.get("judge_critique", []),
        "evidence_that_must_be_preserved": case.get("evidence_that_must_be_preserved", []),
        "proposed_downgrades": downgrades,
        "final_justified_wording": case.get("strongest_justified_rewrite", claim),
    })
    lines = [
        "# Research Judge Report", "", "## 1. Central Claim", claim or "Not supplied.", "",
        "## 2. Strongest Precise Version", case.get("strongest_precise_version", claim or "Not supplied."), "",
        "## 3. Weakest Defensible Version", case.get("weakest_defensible_version", "Not supplied."), "",
        "## 4. Evidence That Must Be Preserved",
    ]
    lines.extend(f"- {item}" for item in (case.get("evidence_that_must_be_preserved", []) or ["None supplied."]))
    lines.extend(["", "## 5. Claim Decomposition", "| Statement | Type | Evidence | Evidence Direction | Evidence Level | Confidence | Main Risk |", "|---|---|---|---|---:|---|---|"])
    for statement in case.get("claim_decomposition", []) or [{"statement": claim, "type": case.get("claim_type", "unspecified"), "evidence": "See scorecard", "risk": "not fully decomposed"}]:
        lines.append(f"| {statement.get('statement', '')} | {statement.get('type', '')} | {statement.get('evidence', '')} | {statement.get('evidence_direction', 'mixed or not supplied')} | {score['evidence_level']} | {score['confidence']} | {statement.get('risk', '')} |")
    for title, content in [
        ("6. Proponent Case", case.get("proponent_case", "Not supplied.")),
        ("7. Judge Critique", case.get("judge_critique", "Not supplied.")),
        ("8. Arbiter Decision", arbiter.get("recommended_verdict")),
        ("9. What Is Actually Supported", case.get("actually_supported", "Not supplied.")),
        ("10. What Is Not Supported", case.get("not_supported", "Not supplied.")),
        ("11. Overclaim Risks", case.get("overclaim_risks", "Not supplied.")),
        ("12. Unsupported Downgrade Risks", case.get("unsupported_downgrade_risks", "Check each objection against the downgrade ledger.")),
    ]:
        lines.extend(["", f"## {title}"])
        lines.extend(f"- {item}" for item in content) if isinstance(content, list) else lines.append(str(content))
    lines.extend(["", "## 13. Alternative Hypotheses", "| Hypothesis | Type | Weakness Addressed | Supported Evidence Explained | Decisive Experiment | Falsifying Result |", "|---|---|---|---|---|---|"])
    for item in alternatives:
        lines.append(f"| {item.get('hypothesis', item.get('name', ''))} | {item.get('type', '')} | {item.get('weakness_addressed', '')} | {item.get('supported_evidence_explained', '')} | {item.get('decisive_experiment', '')} | {item.get('falsifying_result', '')} |")
    lines.extend(["", "## 14. Missing Evidence"])
    lines.extend(f"- {item}" for item in (case.get("missing_evidence", []) or ["None supplied."]))
    lines.extend(["", "## 15. Contradictory Evidence"])
    lines.extend(f"- {item}" for item in (case.get("contradictory_evidence", []) or ["None supplied."]))
    lines.extend(["", "## 16. Downgrade Ledger", render_downgrade_ledger(downgrades or [])])
    lines.extend(["", "## 17. Decisive Tests Ranked by Expected Information Gain"])
    tests = case.get("decisive_tests", [])
    if tests:
        lines.extend(f"- {item.get('name', 'test')}: {item['expected_information_gain_score']}" for item in rank_next_experiments(tests))
    else:
        lines.append("Not supplied.")
    lines.extend(["", "## 18. Alternative Research Directions"])
    lines.extend(f"- {item}" for item in (case.get("alternative_research_directions", []) or ["None supplied."]))
    lines.extend(["", "## 19. Evidence Score", f"Level {score['evidence_level']}: {score['evidence_level_label']} ({score['confidence']})", "", "## 20. Verdict", arbiter.get("recommended_verdict", "not fully evaluated"), "", "## 21. Recommended Next Action", case.get("recommended_next_action", "Run the smallest decisive test that separates the leading alternatives."), "", "## 22. Strongest Justified Rewrite", case.get("strongest_justified_rewrite", claim or "Not supplied.")])
    return "\n".join(lines)
