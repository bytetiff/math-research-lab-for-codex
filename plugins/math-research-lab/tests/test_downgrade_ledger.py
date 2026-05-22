from math_research_lab.judge import downgrade_ledger


def test_valid_justified_downgrade():
    ledger = downgrade_ledger([{
        "original_claim": "The diagnostic change proves mechanism M.",
        "downgraded_claim": "The diagnostic change is consistent with mechanism M.",
        "reason": "mechanism-specific measurement is absent",
        "evidence_basis": "only diagnostic metric was measured",
        "issue_type": "missing evidence",
        "alternative_explanation": "an optimization artifact could move the diagnostic metric",
        "decisive_test": "directly measure M while controlling optimization exposure",
        "supported_evidence_preserved": "diagnostic metric changed in the reported direction",
    }])
    assert ledger["all_justified"] is True


def test_generic_skepticism_downgrade_fails():
    ledger = downgrade_ledger([{
        "original_claim": "The result supports H.",
        "downgraded_claim": "The result is unclear.",
        "reason": "more experiments are needed",
        "evidence_basis": "",
        "issue_type": "",
        "alternative_explanation": "",
        "decisive_test": "",
        "supported_evidence_preserved": "",
    }])
    row = ledger["downgrades"][0]
    assert row["justified"] is False
    assert any("generic skepticism" in problem for problem in row["problems"])
