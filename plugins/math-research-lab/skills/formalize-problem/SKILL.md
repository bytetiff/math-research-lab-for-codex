---
name: formalize-problem
description: Use when a vague mathematical idea, anomaly, algorithm, result, or research claim must be turned into precise objects, assumptions, claims, proof obligations, falsification tests, and minimal validation experiments.
---

# Purpose

Convert informal research material into a precise auditable research object before proof, metric, experiment, or judge work begins.

# When to use

Use when a vague mathematical idea, anomaly, algorithm, result, or research claim must be turned into precise objects, assumptions, claims, proof obligations, falsification tests, and minimal validation experiments.

# Inputs to locate or request

- Problem statement, derivation, result note, paper excerpt, or experimental observation.
- Any supplied notation, formula definitions, raw metric definitions, protocol notes, and data schema.
- Clarify missing domain/codomain/dimension information only when it changes the formal claim.

# Required workflow

1. Extract mathematical and experimental objects with domains, codomains, dimensions, constraints, dependencies, inputs, and outputs.
2. Build a notation table and assumption table; separate explicit assumptions from possible hidden assumptions.
3. Rewrite central claims precisely and classify each as definition, empirical claim, metric result, mechanistic explanation, theoretical claim, implementation claim, speculation, or candidate concept.
4. Generate proof obligations, falsification tests, minimal validation experiments, and unresolved ambiguity.
5. Use scripts/extract_claims.py, scripts/extract_math_objects.py, and scripts/build_assumption_table.py when they improve traceability.

# Required outputs

- Object table.
- Notation table.
- Assumption table.
- Formal claims and claim taxonomy.
- Proof obligations.
- Falsification tests.
- Minimal validation plan.
- Unresolved uncertainty.

# Uncertainty policy

- Separate empirical fact, metric result, mechanism, theory, implementation detail, speculation, and candidate concept.
- Missing evidence may lower confidence but is not contradictory evidence.
- Contradictory evidence may weaken or reject only the specific claim it conflicts with.
- A script result is a measurement or check, not a proof of mechanism or novelty.

# What not to do

- Do not treat a restated claim as validated.
- Do not erase ambiguity; list it.
- Do not promote a candidate concept before concept-disambiguation and research-judge.

# Scripts

- `scripts/build_assumption_table.py`
- `scripts/extract_claims.py`
- `scripts/extract_math_objects.py`

# References

- Read the local `references/` files for this skill and the plugin-level `references/` policy files before producing final judgments.
