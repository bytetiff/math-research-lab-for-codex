---
name: geometry-audit
description: Use to analyze vector geometry, embeddings, prototypes, margins, distances, drift, clusters, and boundary crossings.
---

# Purpose

Measure representation geometry while keeping descriptive statistics separate from mechanisms.

# When to use

Use to analyze vector geometry, embeddings, prototypes, margins, distances, drift, clusters, and boundary crossings.

# Inputs to locate or request

- Feature arrays, labels, logits, before/after arrays, distance or margin definitions, and target metric relationship.

# Required workflow

1. State representation assumptions and feature source.
2. Compute distance, prototype, margin, boundary-crossing, and drift statistics as applicable.
3. Relate geometry to the target metric only as a measured association unless causal isolation is supplied.
4. Use scripts/pairwise_distances.py, scripts/prototype_geometry.py, scripts/margin_analysis.py, and scripts/embedding_drift.py.

# Required outputs

- Feature representation assumptions.
- Distance/prototype statistics.
- Margin definition.
- Margin statistics.
- Boundary-crossing statistics when before/after predictions are available.
- Drift statistics.
- Relationship to target metric.
- Caveats.

# Uncertainty policy

- Separate empirical fact, metric result, mechanism, theory, implementation detail, speculation, and candidate concept.
- Missing evidence may lower confidence but is not contradictory evidence.
- Contradictory evidence may weaken or reject only the specific claim it conflicts with.
- A script result is a measurement or check, not a proof of mechanism or novelty.

# What not to do

- Do not claim geometric patterns are the cause without decisive measurements.
- Do not compare features from incompatible preprocessing pipelines.
- Do not ignore class or group imbalance.

# Scripts

- `scripts/embedding_drift.py`
- `scripts/margin_analysis.py`
- `scripts/pairwise_distances.py`
- `scripts/prototype_geometry.py`

# References

- Read the local `references/` files for this skill and the plugin-level `references/` policy files before producing final judgments.
