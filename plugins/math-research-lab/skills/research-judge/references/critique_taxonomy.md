# Critique Taxonomy

## Metric Substitution
Definition: replacing a target claim with a convenient metric.
Example: claiming a mechanism because a score improved.
Required judge response: accept the metric only as a measurement and ask for mechanism-specific evidence.

## Correlation Substitution
Definition: treating association as causation.
Example: higher alignment co-occurs with accuracy, so alignment caused accuracy.
Required judge response: require causal isolation or direct measurement.

## Protocol Artifact
Definition: protocol differences could explain the result.
Example: different evaluation order or preprocessing.
Required judge response: name the artifact channel and the controlled comparison.

## Optimization Artifact
Definition: unequal training exposure, schedule, tuning, or convergence explains the result.
Example: one method trains longer or receives more tuning.
Required judge response: require equal-budget and exposure-controlled comparison.

## Representation Artifact
Definition: feature extraction, normalization, or representation mismatch explains an observed pattern.
Example: geometry changes because embeddings were normalized differently.
Required judge response: require matched representation pipeline checks.

## Data Artifact
Definition: split overlap, duplicates, leakage, label mismatch, or sampling explains the result.
Example: test items are duplicated in train data.
Required judge response: audit hashes, overlap, labels, and provenance.

## Implementation Artifact
Definition: code, checkpoint, evaluator, hardware, or configuration behavior explains the result.
Example: an evaluator bug changes reported metrics.
Required judge response: compare configs, checkpoints, evaluator versions, and minimal reproductions.

## Baseline Substitution
Definition: a method beats a weak baseline but no equal-budget mechanism-isolating baseline has been used.
Example: improvement is credited to a component when the baseline lacks matching budget or exposure.
Required judge response: cap causal claims and require equal-budget, mechanism-isolating baselines.

## Concept Renaming
Definition: a known phenomenon is renamed as a new concept.
Example: a standard decomposition is given a new theoretical name.
Required judge response: require nearby-concept comparison and literature validation before novelty wording.

## Scope Inflation
Definition: evidence from a narrow protocol is worded as a general law.
Example: one setting is described as universal behavior.
Required judge response: narrow the claim to tested scope unless cross-scope evidence exists.

## Mechanism Overreach
Definition: diagnostic or correlational evidence is stated as a mechanism.
Example: a margin increase is claimed to explain the whole effect without direct test.
Required judge response: classify as diagnostic only or promising but unproven.

## Novelty Inflation
Definition: a candidate framing is treated as new without literature validation.
Example: claiming a new principle from one empirical pattern.
Required judge response: require literature validation and replicated evidence.

## Unsupported Skepticism
Definition: rejecting or weakening a claim without a concrete flaw, missing measurement, contradictory result, or meaningful alternative.
Example: saying the evidence is insufficient without naming the required measurement.
Required judge response: mark the objection unsupported and preserve the strongest defensible claim.
