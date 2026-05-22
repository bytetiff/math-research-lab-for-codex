from math_research_lab.judge import compare_hypotheses


def test_hypothesis_comparison_preserves_tie():
    result = compare_hypotheses({
        "hypotheses": [
            {"name": "A", "supporting_evidence": ["obs1"], "missing_evidence": [], "contradictory_evidence": []},
            {"name": "B", "supporting_evidence": ["obs1"], "missing_evidence": [], "contradictory_evidence": []},
        ]
    })
    assert result["tie"] is True
    assert result["winner"] is None
