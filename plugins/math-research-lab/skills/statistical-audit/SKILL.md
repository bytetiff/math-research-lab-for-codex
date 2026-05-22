---
name: statistical-audit
description: Use to assess empirical evidence strength, uncertainty, confidence intervals, effect sizes, permutation tests, bootstrap tests, and seed sensitivity.
---

# Purpose

Quantify uncertainty and distinguish exploratory correlations from confirmatory claims.

# When to use

Use to assess empirical evidence strength, uncertainty, confidence intervals, effect sizes, permutation tests, bootstrap tests, and seed sensitivity.

# Inputs to locate or request

- CSV or tabular data.
- Metric definition, sample unit, replication structure, grouping, seeds, and protocol scope.

# Required workflow

1. Identify the experimental unit and metric definition.
2. Check replication structure and estimate uncertainty.
3. Compute confidence intervals, effect size, bootstrap or permutation tests where appropriate.
4. Check sensitivity to seeds, orders, subsets, or configurations.
5. Distinguish exploratory correlation from confirmatory testing.
6. Use scripts/bootstrap_ci.py, scripts/permutation_test.py, scripts/effect_size.py, and scripts/seed_sensitivity.py.

# Required outputs

- Metric and sample unit.
- Number of observations.
- Uncertainty.
- Confidence interval.
- Effect size.
- Sensitivity findings.
- Inference limits.
- Conclusion strength.

# Uncertainty policy

- Separate empirical fact, metric result, mechanism, theory, implementation detail, speculation, and candidate concept.
- Missing evidence may lower confidence but is not contradictory evidence.
- Contradictory evidence may weaken or reject only the specific claim it conflicts with.
- A script result is a measurement or check, not a proof of mechanism or novelty.

# What not to do

- Do not treat statistical association as causation.
- Do not ignore small replication count warnings.
- Do not collapse exploratory and confirmatory analyses.

# Scripts

- `scripts/bootstrap_ci.py`
- `scripts/effect_size.py`
- `scripts/permutation_test.py`
- `scripts/seed_sensitivity.py`

# References

- Read the local `references/` files for this skill and the plugin-level `references/` policy files before producing final judgments.
