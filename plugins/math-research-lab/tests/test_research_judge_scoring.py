from math_research_lab.judge import score_research_claim


def test_mechanism_claim_without_direct_measurement_not_high_confidence():
    result = score_research_claim({
        "claim": "The result is caused by mechanism M.",
        "claim_type": "mechanism",
        "evidence_items": [{"type": "controlled ablation"}],
        "missing_evidence": ["direct mechanism measurement"],
    })
    assert result["evidence_level"] == 3
    assert result["confidence"] == "medium"
    assert result["missing_is_not_contradictory"] is True


def test_novelty_claim_capped_without_literature_validation():
    result = score_research_claim({
        "claim_type": "novelty",
        "evidence_items": [{"type": "replicated mechanism"}],
        "literature_validated": False,
    })
    assert result["evidence_level"] == 2
    assert "novelty claim lacks literature validation" in result["caps_applied"]
