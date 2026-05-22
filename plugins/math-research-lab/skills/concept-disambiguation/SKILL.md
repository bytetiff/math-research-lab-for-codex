---
name: concept-disambiguation
description: Use to prevent renaming, concept substitution, terminology inflation, and false novelty in candidate research concepts.
---

# Purpose

Separate metric, mechanism, method, implementation, observation, theory, speculation, and candidate concept claims.

# When to use

Use to prevent renaming, concept substitution, terminology inflation, and false novelty in candidate research concepts.

# Inputs to locate or request

- Candidate concept definition.
- Nearby concepts, risky terminology, forbidden wording, and evidence scope.

# Required workflow

1. Identify the candidate concept and decompose its claim parts.
2. Compare against nearby concepts and decide whether it is a renamed known concept, special case, combination, diagnostic decomposition, empirical pattern, useful candidate framing, or unsupported.
3. Produce forbidden wording and cautious allowed wording.
4. Use scripts/concept_overlap_table.py, scripts/terminology_risk_report.py, and scripts/forbidden_wording_check.py.

# Required outputs

- Candidate concept.
- Overlap table.
- Distinction table.
- Substitution risk.
- Forbidden wording.
- Cautious allowed wording.
- Verdict.

# Uncertainty policy

- Separate empirical fact, metric result, mechanism, theory, implementation detail, speculation, and candidate concept.
- Missing evidence may lower confidence but is not contradictory evidence.
- Contradictory evidence may weaken or reject only the specific claim it conflicts with.
- A script result is a measurement or check, not a proof of mechanism or novelty.

# What not to do

- Do not claim novelty without literature validation.
- Do not replace a mechanism with a metric name.
- Do not allow concept substitution to inflate the result.

# Scripts

- `scripts/concept_overlap_table.py`
- `scripts/forbidden_wording_check.py`
- `scripts/terminology_risk_report.py`

# References

- Read the local `references/` files for this skill and the plugin-level `references/` policy files before producing final judgments.
