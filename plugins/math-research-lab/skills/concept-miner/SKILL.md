---
name: concept-miner
description: Use to detect recurring empirical or theoretical patterns and formulate cautious candidate concepts without claiming novelty.
---

# Purpose

Convert recurrent patterns into operational candidate framings that can be disambiguated and judged.

# When to use

Use to detect recurring empirical or theoretical patterns and formulate cautious candidate concepts without claiming novelty.

# Inputs to locate or request

- Observed pattern, repeated measurements, protocol scope, affected objects, and nearby known concepts if available.

# Required workflow

1. Identify the recurrent pattern and classify its category.
2. Decide whether a provisional name is useful.
3. Draft an operational definition, observables, falsification tests, and likely overlap categories.
4. Assign status: known, likely known under another name, weakly explored, candidate new framing, potentially novel but unverified, or unsupported speculation.
5. Require concept-disambiguation and research-judge before stronger use.
6. Use scripts/pattern_discovery.py, scripts/hypothesis_graph.py, and scripts/concept_report.py.

# Required outputs

- Pattern.
- Candidate name if justified.
- Operational definition.
- Observables.
- Falsification tests.
- Nearby concepts.
- Status.
- Evidence still needed.

# Uncertainty policy

- Separate empirical fact, metric result, mechanism, theory, implementation detail, speculation, and candidate concept.
- Missing evidence may lower confidence but is not contradictory evidence.
- Contradictory evidence may weaken or reject only the specific claim it conflicts with.
- A script result is a measurement or check, not a proof of mechanism or novelty.

# What not to do

- Do not declare novelty.
- Do not name a concept when the name adds no audit value.
- Do not bypass disambiguation.

# Scripts

- `scripts/concept_report.py`
- `scripts/hypothesis_graph.py`
- `scripts/pattern_discovery.py`

# References

- Read the local `references/` files for this skill and the plugin-level `references/` policy files before producing final judgments.
