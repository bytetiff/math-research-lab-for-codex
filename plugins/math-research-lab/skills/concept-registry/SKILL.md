---
name: concept-registry
description: Use to create and update auditable markdown records for candidate concepts under research_notes/concept_registry/.
---

# Purpose

Persist candidate concepts with status, evidence, missing evidence, contradictions, safe wording, and judge verdicts.

# When to use

Use to create and update auditable markdown records for candidate concepts under research_notes/concept_registry/.

# Inputs to locate or request

- Structured concept JSON.
- Evidence updates, literature-validation state, status, and judge verdict.

# Required workflow

1. Validate status against evidence level and literature-validation state.
2. Create or update a markdown record under research_notes/concept_registry/.
3. Preserve history when updating evidence.
4. Keep missing evidence separate from contradictory evidence.
5. Use scripts/create_concept_record.py, scripts/update_evidence_table.py, and scripts/concept_status_check.py.

# Required outputs

- Concept record path.
- Evidence table update.
- Status validation.
- History-preserving markdown record.

# Uncertainty policy

- Separate empirical fact, metric result, mechanism, theory, implementation detail, speculation, and candidate concept.
- Missing evidence may lower confidence but is not contradictory evidence.
- Contradictory evidence may weaken or reject only the specific claim it conflicts with.
- A script result is a measurement or check, not a proof of mechanism or novelty.

# What not to do

- Do not mark a concept as novel without explicit literature validation.
- Do not delete prior evidence history.
- Do not treat missing evidence as contradictory.

# Scripts

- `scripts/concept_status_check.py`
- `scripts/create_concept_record.py`
- `scripts/update_evidence_table.py`

# References

- Read the local `references/` files for this skill and the plugin-level `references/` policy files before producing final judgments.
