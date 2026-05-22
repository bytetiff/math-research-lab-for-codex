---
name: experiment-audit
description: Use to audit data splits, duplicates, provenance, configs, checkpoints, evaluators, seeds, resource budgets, and reproducibility risks.
---

# Purpose

Check whether the empirical result is valid enough to interpret.

# When to use

Use to audit data splits, duplicates, provenance, configs, checkpoints, evaluators, seeds, resource budgets, and reproducibility risks.

# Inputs to locate or request

- Split files, artifact paths, configs, run records, result CSVs, checkpoint/evaluator notes, and protocol description.

# Required workflow

1. Summarize the protocol and artifacts.
2. Check duplicate files, duplicate hashes, split overlap, preprocessing mismatch, label mapping inconsistency, checkpoint mismatch, evaluator mismatch, config differences, seed mismatch, resource-budget mismatch, unequal optimization exposure, unequal memory budget, and missing provenance when applicable.
3. List channels that were not testable from supplied artifacts.
4. Use scripts/check_split_overlap.py, scripts/hash_duplicates.py, scripts/config_diff.py, and scripts/result_reproducibility_check.py.

# Required outputs

- Protocol summary.
- Artifact checks run.
- Findings.
- Untested artifact channels.
- Reproducibility risks.
- Required corrections.
- Validity verdict.

# Uncertainty policy

- Separate empirical fact, metric result, mechanism, theory, implementation detail, speculation, and candidate concept.
- Missing evidence may lower confidence but is not contradictory evidence.
- Contradictory evidence may weaken or reject only the specific claim it conflicts with.
- A script result is a measurement or check, not a proof of mechanism or novelty.

# What not to do

- Do not call a result an artifact without naming the artifact channel.
- Do not infer protocol validity from final metrics only.
- Do not treat missing provenance as contradictory evidence unless it conflicts with a claim.

# Scripts

- `scripts/check_split_overlap.py`
- `scripts/config_diff.py`
- `scripts/hash_duplicates.py`
- `scripts/result_reproducibility_check.py`

# References

- Read the local `references/` files for this skill and the plugin-level `references/` policy files before producing final judgments.
