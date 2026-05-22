# Math Research Lab

Math Research Lab is a domain-agnostic Codex plugin for mathematical and scientific research auditing. It helps Codex formalize vague research ideas, audit notation and assumptions, critique derivations, validate symbolic and numerical claims, audit metrics and experiments, analyze statistics, geometry, spectra, and optimization traces, govern candidate concepts, and produce balanced research judgments.

It does not ship subject-specific adapters. Any domain-specific formula, metric, definition, protocol, or data interpretation must be supplied by the user at runtime.

## Non-Negotiable Principles

```text
Never treat a metric result as a proven mechanism.
Never treat correlation as causation.
Never claim novelty without literature validation.
Never propose improvements before result validity is checked.
Never downgrade a claim through generic skepticism.
Never reject a claim merely because required evidence is missing.
Missing evidence lowers confidence; contradictory evidence challenges validity.
Any alternative explanation must preserve and explain already supported observations.
```

## Architecture

1. Formalization and validation: `formalize-problem`, `notation-audit`, `proof-audit`, `numerical-validation`, `statistical-audit`, `metric-audit`, `experiment-audit`, `geometry-audit`, `spectral-audit`, and `optimization-audit`.
2. Concept governance: `concept-miner`, `concept-disambiguation`, and `concept-registry`.
3. Balanced research judgment: `research-judge`.

## Skills

- `formalize-problem`: turn vague ideas, anomalies, and claims into objects, assumptions, formal claims, proof obligations, falsification tests, and validation plans.
- `notation-audit`: detect overloaded symbols, undefined notation, unclear indices, and dimension or codomain gaps.
- `proof-audit`: inspect derivations, implication steps, boundary cases, symbolic identities, numerical checks, and corrected statements.
- `numerical-validation`: run finite-difference, gradient, property, stability, and sensitivity checks.
- `statistical-audit`: estimate uncertainty, confidence intervals, effect sizes, permutation tests, bootstrap intervals, and seed sensitivity.
- `metric-audit`: verify generic user-defined metrics and matrix-derived measurements without hard-coding domain metrics.
- `experiment-audit`: check splits, duplicates, configs, checkpoints, evaluators, seeds, budgets, exposure, and provenance.
- `geometry-audit`: analyze distances, prototypes, margins, drift, and boundary crossings.
- `spectral-audit`: analyze SVD energy, effective rank, entropy, and low-rank reconstruction.
- `optimization-audit`: audit loss curves, convergence, gradient norms, instability, exposure, and sensitivity.
- `concept-miner`: formulate cautious candidate concepts from recurring patterns without claiming novelty.
- `concept-disambiguation`: compare candidate concepts against nearby concepts and produce forbidden plus safe wording.
- `concept-registry`: create auditable markdown concept records under `research_notes/concept_registry/`.
- `research-judge`: produce balanced proponent, critique, and arbiter judgments with evidence levels and decisive next tests.

## Scripts

Each skill has a `scripts/` directory. Scripts expose CLIs and import reusable functions from `src/math_research_lab/`. They compute concrete artifacts such as JSON reports, markdown tables, confidence intervals, metric audits, margin summaries, concept records, downgrade ledgers, and judge reports. Script outputs are measurements or structured checks; they never claim more than they compute.

## Candidate Concepts

Candidate concepts are stored under:

```text
research_notes/concept_registry/
```

Each record includes status, created/updated date, operational definition, observed pattern, evidence table, evidence level, nearby concepts, distinctions, falsification tests, contradictory evidence, missing evidence, forbidden wording, safe wording, decisive experiments, and judge verdict. History is preserved when evidence is updated.

## Research Judge

The judge avoids both overclaiming and unsupported skepticism. It downgrades a claim only when a concrete basis is identified: missing measurement required by the claim type, specific alternative hypothesis, contradictory evidence, artifact risk, scope mismatch, nearby known concept weakening novelty, or decisive failed test.

Missing evidence is not contradictory evidence. Rejection requires contradiction, failed falsification, or lack of operational definition.

## Run Tests

```bash
python -m pytest -q
```

Run this from `plugins/math-research-lab` after installing the declared dependencies.

## Install From This Repository

Install the marketplace from the repository root, not from this plugin package directory:

```powershell
codex plugin marketplace add C:\math-research-lab
```

Then run `/plugins` in Codex and enable `math-research-lab`.
