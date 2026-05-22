---
name: notation-audit
description: Use to find ambiguous mathematical notation, overloaded symbols, dimension mismatches, unclear indices, inconsistent terminology, and undefined objects.
---

# Purpose

Make notation explicit enough that later proof, metric, numerical, or experimental checks can be reproduced.

# When to use

Use to find ambiguous mathematical notation, overloaded symbols, dimension mismatches, unclear indices, inconsistent terminology, and undefined objects.

# Inputs to locate or request

- Text, derivation, symbol list, formula fragments, or JSON symbol metadata.
- Known domains, codomains, dimensions, units, indices, and conventions.

# Required workflow

1. Extract or ingest symbols and formula fragments.
2. Identify reused symbols, undefined objects, overloaded terms, unclear indices, and dimension or codomain gaps.
3. Build a notation table, dimension table, index convention table, and correction suggestions.
4. Use scripts/check_symbol_reuse.py, scripts/build_notation_table.py, and scripts/dimension_table.py for reproducible tables.

# Required outputs

- Notation table.
- Symbol conflicts.
- Dimension/codomain table.
- Index convention table.
- Ambiguous terms.
- Corrected notation suggestions.

# Uncertainty policy

- Separate empirical fact, metric result, mechanism, theory, implementation detail, speculation, and candidate concept.
- Missing evidence may lower confidence but is not contradictory evidence.
- Contradictory evidence may weaken or reject only the specific claim it conflicts with.
- A script result is a measurement or check, not a proof of mechanism or novelty.

# What not to do

- Do not infer semantic meaning from notation alone.
- Do not silently choose between conflicting conventions.
- Do not claim dimension consistency unless every required object is defined.

# Scripts

- `scripts/build_notation_table.py`
- `scripts/check_symbol_reuse.py`
- `scripts/dimension_table.py`

# References

- Read the local `references/` files for this skill and the plugin-level `references/` policy files before producing final judgments.
