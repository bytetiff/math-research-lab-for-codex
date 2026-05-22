---
name: spectral-audit
description: Use to analyze SVD, eigenvalues, spectral energy, entropy, effective rank, low-rank reconstruction, and subspace coverage.
---

# Purpose

Measure spectral structure without overinterpreting it as mechanism or novelty.

# When to use

Use to analyze SVD, eigenvalues, spectral energy, entropy, effective rank, low-rank reconstruction, and subspace coverage.

# Inputs to locate or request

- Matrix or singular/eigenvalue arrays.
- Rank choices, decomposition target, normalization, and comparison object if any.

# Required workflow

1. Define the matrix or operator being decomposed.
2. Compute singular or eigenvalue summaries, retained energy, effective rank, spectral entropy, reconstruction error, and subspace comparison where supplied.
3. State what the spectral result does and does not imply.
4. Use scripts/svd_energy.py, scripts/effective_rank.py, scripts/spectral_entropy.py, and scripts/low_rank_reconstruction.py.

# Required outputs

- Matrix/object being decomposed.
- Singular/eigenvalue summary.
- Retained energy.
- Effective rank.
- Spectral entropy.
- Reconstruction error.
- Subspace comparison where appropriate.
- Interpretation limits.

# Uncertainty policy

- Separate empirical fact, metric result, mechanism, theory, implementation detail, speculation, and candidate concept.
- Missing evidence may lower confidence but is not contradictory evidence.
- Contradictory evidence may weaken or reject only the specific claim it conflicts with.
- A script result is a measurement or check, not a proof of mechanism or novelty.

# What not to do

- Do not equate low rank with causal compression.
- Do not claim spectral structure is novel without literature validation.
- Do not hide rank-selection sensitivity.

# Scripts

- `scripts/effective_rank.py`
- `scripts/low_rank_reconstruction.py`
- `scripts/spectral_entropy.py`
- `scripts/svd_energy.py`

# References

- Read the local `references/` files for this skill and the plugin-level `references/` policy files before producing final judgments.
