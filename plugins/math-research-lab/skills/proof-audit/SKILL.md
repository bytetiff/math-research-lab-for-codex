---
name: proof-audit
description: Use to critically inspect derivations, proof sketches, lemmas, equivalence arguments, convergence arguments, gradient derivations, or mathematical explanations.
---

# Purpose

Separate proofs from conditional derivations, plausibility arguments, and intuition.

# When to use

Use to critically inspect derivations, proof sketches, lemmas, equivalence arguments, convergence arguments, gradient derivations, or mathematical explanations.

# Inputs to locate or request

- Exact claim and derivation text.
- Definitions, assumptions, domains, boundary cases, and any target identities or predicates.

# Required workflow

1. Parse the exact claim and enumerate assumptions.
2. Break the derivation into implication steps and mark each valid, unsupported, invalid, or conditionally valid.
3. Search for counterexamples and boundary cases.
4. Use symbolic checks when possible and numerical checks when possible.
5. Separate proof, derivation under assumptions, plausibility argument, and intuition.
6. Provide the strongest corrected statement supported by the analysis.
7. Use scripts/verify_sympy_identity.py, scripts/finite_difference_check.py, scripts/search_counterexamples.py, and scripts/implication_checklist.py.

# Required outputs

- Claim.
- Assumptions.
- Checked steps.
- Hidden assumptions.
- Counterexamples or failed search statement.
- Verification procedures.
- Corrected claim.
- Verdict.

# Uncertainty policy

- Separate empirical fact, metric result, mechanism, theory, implementation detail, speculation, and candidate concept.
- Missing evidence may lower confidence but is not contradictory evidence.
- Contradictory evidence may weaken or reject only the specific claim it conflicts with.
- A script result is a measurement or check, not a proof of mechanism or novelty.

# What not to do

- Do not treat numerical agreement as proof.
- Do not reject a claim because a search failed to prove it.
- Do not strengthen a theorem beyond its assumptions.

# Scripts

- `scripts/finite_difference_check.py`
- `scripts/implication_checklist.py`
- `scripts/search_counterexamples.py`
- `scripts/verify_sympy_identity.py`

# References

- Read the local `references/` files for this skill and the plugin-level `references/` policy files before producing final judgments.
