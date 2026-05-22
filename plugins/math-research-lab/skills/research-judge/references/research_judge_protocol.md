# Research Judge Protocol

Central question:

What exactly has been shown, what has merely been made plausible, what is contradicted, and what evidence would strengthen, weaken, or reject the interpretation?

## Stance

The judge is evidence-bound and adversarial in a balanced way. It must neither defend the claim automatically nor weaken it automatically. It must preserve supported evidence while identifying real overclaims, concrete alternatives, artifact risks, and missing decisive measurements.

## Workflow

1. Identify the central claim.
2. Split mixed claims.
3. Rewrite the central claim in the strongest precise version and weakest defensible version.
4. Classify subclaims as empirical fact, metric result, mechanistic explanation, theoretical claim, implementation detail, speculation, or candidate concept.
5. List evidence any alternative explanation must preserve.
6. Evaluate evidence for each subclaim.
7. Classify evidence direction as supporting, neutral, missing, contradictory, or artifact-risk.
8. Evaluate overclaim risks.
9. Evaluate unsupported-downgrade risks.
10. Generate competing alternative hypotheses.
11. Identify the smallest decisive experiment for each major ambiguity.
12. Rank experiments by expected information gain.
13. Produce an arbiter decision.
14. Provide the strongest justified rewritten claim.

## Balanced Three-Role Structure

- Proponent Case: strongest supporting evidence, what must not be discarded, strongest defensible version.
- Judge Critique: real overclaims, concrete alternatives, artifact risks, missing decisive measurements, justified downgrades only.
- Arbiter Decision: valid objections, unsupported objections, preserved evidence, evidence level, verdict, strongest final wording.

## Report Structure

Use `judge_output_template.md` exactly for full reports.

## Verdict Rules

Use exactly one verdict: supported, weakly supported, diagnostic only, promising but unproven, likely artifact, rejected, or not fully evaluated.

`likely artifact` requires a specific artifact channel and evidence supporting that channel.

`rejected` requires contradictory evidence, a failed decisive falsification test, or lack of operational definition.

## No Unsupported Downgrade Rule

A downgrade is valid only if it identifies a concrete basis: missing measurement required by the claim type, specific alternative hypothesis, contradictory evidence, artifact risk, scope mismatch, nearby known concept weakening novelty, or decisive failed test. If the basis cannot be stated, do not downgrade. Mark the claim not fully evaluated.

## Missing Versus Contradictory Evidence Rule

Missing evidence lowers confidence. Contradictory evidence may weaken a claim. Only contradictory evidence or failed decisive tests may justify rejection.

## Preserve Supported Evidence

Every alternative and downgrade must preserve and explain the supported observations unless it explicitly shows that those observations are invalid.

## Decisive Experiments

Never say only that more experiments are needed. Name the smallest experiment that would distinguish alternatives, falsify the claim, or directly measure the mechanism.

## No Generic Writing Advice

The judge is not a copy editor. Do not merely soften prose. Explain what the evidence supports and why.
