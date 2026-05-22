---
name: optimization-audit
description: Use to analyze loss curves, convergence, gradients, plateaus, sensitivity, instability, additional optimization exposure, and hyperparameter-driven artifacts.
---

# Purpose

Identify optimization artifacts and exposure differences before interpreting empirical improvements.

# When to use

Use to analyze loss curves, convergence, gradients, plateaus, sensitivity, instability, additional optimization exposure, and hyperparameter-driven artifacts.

# Inputs to locate or request

- Loss/metric traces, gradient norms, hyperparameter sweeps, budgets, steps, epochs, and comparison protocols.

# Required workflow

1. Summarize optimization traces and budgets.
2. Check convergence, spikes, plateaus, instability, gradient norms, local sensitivity, and unequal exposure.
3. Recommend controlled comparisons that isolate optimization effects.
4. Use scripts/loss_curve_audit.py, scripts/convergence_diagnostics.py, scripts/gradient_norms.py, and scripts/local_sensitivity.py.

# Required outputs

- Optimization trace summary.
- Convergence diagnostics.
- Gradient statistics.
- Exposure/budget comparison.
- Sensitivity findings.
- Optimization-artifact risks.
- Recommendations for controlled comparisons.

# Uncertainty policy

- Separate empirical fact, metric result, mechanism, theory, implementation detail, speculation, and candidate concept.
- Missing evidence may lower confidence but is not contradictory evidence.
- Contradictory evidence may weaken or reject only the specific claim it conflicts with.
- A script result is a measurement or check, not a proof of mechanism or novelty.

# What not to do

- Do not treat extra optimization exposure as a method mechanism.
- Do not compare runs with unequal budgets without labeling the risk.
- Do not infer convergence from a final checkpoint only.

# Scripts

- `scripts/convergence_diagnostics.py`
- `scripts/gradient_norms.py`
- `scripts/local_sensitivity.py`
- `scripts/loss_curve_audit.py`

# References

- Read the local `references/` files for this skill and the plugin-level `references/` policy files before producing final judgments.
