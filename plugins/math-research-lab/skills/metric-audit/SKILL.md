---
name: metric-audit
description: Use to audit any reported metric, especially generic metrics computed from matrices, sequences, grouped results, checkpoints, or decompositions.
---

# Purpose

Verify the user-supplied metric definition and computation before interpreting the result.

# When to use

Use to audit any reported metric, especially generic metrics computed from matrices, sequences, grouped results, checkpoints, or decompositions.

# Inputs to locate or request

- User-provided metric definition.
- Raw data, matrix/table schema, indexing rules, exclusions, aggregation rules, and units.

# Required workflow

1. Obtain the user-provided definition before computing.
2. Identify inputs, indexing, exclusions, aggregation rules, and units.
3. Recompute from raw data when possible.
4. Check missing cells, duplicate cells, incorrect baselines, incorrect final indices, included/excluded items, and averaging conventions.
5. Decompose the metric only when mathematically valid and label it as algebraic or accounting decomposition.
6. Compare alternative reasonable definitions only when clearly labeled.
7. Use scripts/metric_matrix_audit.py, scripts/recompute_metric_from_csv.py, scripts/decompose_metric_contributions.py, and scripts/compare_metric_definitions.py.

# Required outputs

- Metric definition.
- Input schema.
- Recomputed metric.
- Discrepancy table.
- Contribution decomposition.
- Aggregation caveats.
- Interpretation boundary.
- Verdict.

# Uncertainty policy

- Separate empirical fact, metric result, mechanism, theory, implementation detail, speculation, and candidate concept.
- Missing evidence may lower confidence but is not contradictory evidence.
- Contradictory evidence may weaken or reject only the specific claim it conflicts with.
- A script result is a measurement or check, not a proof of mechanism or novelty.

# What not to do

- Do not hard-code a domain-specific metric.
- Do not treat metric decomposition as a mechanism.
- Do not recommend improvements before result validity is checked.

# Scripts

- `scripts/compare_metric_definitions.py`
- `scripts/decompose_metric_contributions.py`
- `scripts/metric_matrix_audit.py`
- `scripts/recompute_metric_from_csv.py`

# References

- Read the local `references/` files for this skill and the plugin-level `references/` policy files before producing final judgments.
