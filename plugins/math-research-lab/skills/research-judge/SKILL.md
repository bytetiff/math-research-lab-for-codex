---
name: research-judge
description: Use after a claim, result, mechanism, metric, explanation, or candidate concept has been produced and needs balanced evidence-bound adversarial judgment.
---

# Purpose

Decide what has been shown, what is plausible, what is contradicted, and which evidence would strengthen, weaken, or reject the interpretation.

# When to use

Use after a claim, result, mechanism, metric, explanation, or candidate concept has been produced and needs balanced evidence-bound adversarial judgment.

# Inputs to locate or request

- Central claim and subclaims.
- Evidence items, missing evidence, contradictory evidence, artifact risks, alternatives, and proposed downgrades.
- The exact supported observations that alternatives must preserve.

# Required workflow

1. Identify and split mixed claims.
2. Rewrite strongest precise and weakest defensible versions.
3. Classify subclaims and evidence direction.
4. Evaluate overclaim risks and unsupported-downgrade risks.
5. Generate alternative hypotheses that preserve supported evidence.
6. Name the smallest decisive experiment for each major ambiguity and rank by expected information gain.
7. Produce proponent case, judge critique, and arbiter decision.
8. Use scripts/score_research_claim.py, scripts/build_critique_report.py, scripts/compare_hypotheses.py, scripts/rank_next_experiments.py, scripts/downgrade_ledger.py, and scripts/arbiter_check.py.

# Required outputs

- Fixed Research Judge Report structure.
- Evidence score.
- Alternative hypotheses table.
- Downgrade ledger.
- Arbiter verdict.
- Strongest justified rewrite.

# Uncertainty policy

- Separate empirical fact, metric result, mechanism, theory, implementation detail, speculation, and candidate concept.
- Missing evidence may lower confidence but is not contradictory evidence.
- Contradictory evidence may weaken or reject only the specific claim it conflicts with.
- A script result is a measurement or check, not a proof of mechanism or novelty.

# What not to do

- Do not defend the claim automatically.
- Do not weaken the claim automatically.
- Do not downgrade without concrete evidence-bound justification.
- Do not reject without contradiction, failed falsification, or lack of operational definition.

# Scripts

- `scripts/arbiter_check.py`
- `scripts/build_critique_report.py`
- `scripts/compare_hypotheses.py`
- `scripts/downgrade_ledger.py`
- `scripts/rank_next_experiments.py`
- `scripts/score_research_claim.py`

# References

- Read the local `references/` files for this skill and the plugin-level `references/` policy files before producing final judgments.
