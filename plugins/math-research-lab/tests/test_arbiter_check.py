from math_research_lab.judge import arbiter_check


def test_arbiter_preserves_supported_evidence_and_flags_ignored_items():
    result = arbiter_check({
        "central_claim": "H is supported.",
        "proponent_case": ["metric improved"],
        "judge_critique": "A concrete missing measurement is noted but metric improved is preserved.",
        "evidence_that_must_be_preserved": ["metric improved", "replicated across seeds"],
        "proposed_downgrades": [{
            "original_claim": "H is proven.",
            "downgraded_claim": "H is supported as a diagnostic observation.",
            "reason": "direct mechanism measurement is absent",
            "evidence_basis": "metric evidence only",
            "issue_type": "missing evidence",
            "alternative_explanation": "protocol-level diagnostic explanation",
            "decisive_test": "measure the mechanism directly",
            "supported_evidence_preserved": "metric improved",
        }],
    })
    assert result["preserved_evidence"] == ["metric improved", "replicated across seeds"]
    assert result["valid_objections"]
    assert result["evidence_ignored_by_judge"] == ["replicated across seeds"]
