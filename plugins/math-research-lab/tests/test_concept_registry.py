from pathlib import Path

from math_research_lab.concepts import concept_status_check, create_concept_record, update_evidence_table


def test_concept_record_creation_under_registry(tmp_path: Path):
    concept = {
        "name": "Candidate Pattern",
        "status": "candidate new framing",
        "operational_definition": "A repeated measurable relation under a stated protocol.",
        "observed_pattern": "Metric and diagnostic move together across runs.",
        "evidence_level": 2,
    }
    path = create_concept_record(concept, tmp_path)
    assert path == tmp_path / "research_notes" / "concept_registry" / "candidate-pattern.md"
    text = path.read_text(encoding="utf-8")
    assert "Candidate Pattern" in text
    assert "Missing Evidence" in text


def test_concept_record_update_preserves_history(tmp_path: Path):
    path = create_concept_record({"name": "Update Pattern"}, tmp_path)
    update_evidence_table(path, [{"evidence": "new check", "type": "metric", "direction": "supporting", "level": 2, "note": "diagnostic"}])
    text = path.read_text(encoding="utf-8")
    assert "Evidence Update" in text
    assert "Record created or updated" in text


def test_concept_status_constraints():
    invalid = concept_status_check("novel", evidence_level=2, literature_validated=False)
    assert invalid["valid"] is False
    assert "Novelty status requires explicit literature validation." in invalid["errors"]
    cautious = concept_status_check("potentially novel but unverified", evidence_level=2, literature_validated=False)
    assert cautious["valid"] is True
    assert cautious["warnings"]
