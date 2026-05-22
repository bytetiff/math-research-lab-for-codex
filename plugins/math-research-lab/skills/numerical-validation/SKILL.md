---
name: numerical-validation
description: Use to run reproducible numerical tests for mathematical or algorithmic claims, including property tests, gradient checks, finite differences, stability sweeps, and sensitivity checks.
---

# Purpose

Measure numerical consistency and robustness without overstating the result as proof or mechanism.

# When to use

Use to run reproducible numerical tests for mathematical or algorithmic claims, including property tests, gradient checks, finite differences, stability sweeps, and sensitivity checks.

# Inputs to locate or request

- Tested property or invariant.
- Numeric inputs, tolerances, seeds, ranges, and expected values.
- Implementation-independent definition of what failure means.

# Required workflow

1. Define the property and invariant before running tests.
2. Set a seed, tolerance, sample range, and failure policy.
3. Run randomized property tests, finite-difference checks, gradient checks, stability sweeps, or sensitivity checks as appropriate.
4. Report failures, tolerances, and interpretation limits.
5. Use scripts/randomized_property_test.py, scripts/gradient_check.py, and scripts/stability_sweep.py.

# Required outputs

- Tested property.
- Mathematical invariant.
- Test design.
- Random seed policy.
- Result.
- Numerical tolerance.
- Failures.
- Interpretation limits.

# Uncertainty policy

- Separate empirical fact, metric result, mechanism, theory, implementation detail, speculation, and candidate concept.
- Missing evidence may lower confidence but is not contradictory evidence.
- Contradictory evidence may weaken or reject only the specific claim it conflicts with.
- A script result is a measurement or check, not a proof of mechanism or novelty.

# What not to do

- Do not execute arbitrary unsafe user code.
- Do not claim that passing random tests proves a theorem.
- Do not hide tolerance choices.

# Scripts

- `scripts/gradient_check.py`
- `scripts/randomized_property_test.py`
- `scripts/stability_sweep.py`

# References

- Read the local `references/` files for this skill and the plugin-level `references/` policy files before producing final judgments.
