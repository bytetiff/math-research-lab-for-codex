from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from . import concepts, experiments, geometry, judge, metrics, numerics, optimization, spectral, stats, text_tools
from .cli_utils import load_json, read_csv_checked, read_text_or_file, write_json_output, write_text_output
from .safe_expr import evaluate_expression


def _csv_numbers(raw: str) -> list[float]:
    return [float(part.strip()) for part in raw.split(",") if part.strip()]


def _csv_strings(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def _parser(command: str) -> argparse.ArgumentParser:
    return argparse.ArgumentParser(prog=command, description=f"Math Research Lab utility: {command}")


def main(command: str | None = None, argv: list[str] | None = None) -> int:
    '''Run the CLI for one generated script command.'''
    if command is None:
        raise ValueError("script command must be supplied by wrapper")
    parser = _parser(command)

    if command in {"extract_claims", "extract_math_objects", "build_assumption_table", "check_symbol_reuse", "implication_checklist", "terminology_risk_report"}:
        parser.add_argument("input")
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        text = read_text_or_file(args.input)
        if command == "extract_claims":
            return _json(text_tools.extract_claims(text), args.output)
        if command == "extract_math_objects":
            return _json(text_tools.extract_math_objects(text), args.output)
        if command == "build_assumption_table":
            return _text(text_tools.build_assumption_table(text), args.output)
        if command == "check_symbol_reuse":
            return _json(text_tools.check_symbol_reuse(text), args.output)
        if command == "implication_checklist":
            return _text(text_tools.implication_checklist(text), args.output)
        return _json(text_tools.terminology_risks(text), args.output)

    if command == "build_notation_table":
        parser.add_argument("input", help="JSON symbol list or text/markdown to extract symbols from")
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        input_path = Path(args.input)
        if input_path.exists() and input_path.suffix.lower() == ".json":
            symbols = load_json(args.input)
        else:
            symbols = text_tools.extract_math_objects(read_text_or_file(args.input))["symbols"]
        return _text(text_tools.build_notation_table(symbols), args.output)

    if command == "dimension_table":
        parser.add_argument("metadata_json")
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        return _text(text_tools.dimension_table(load_json(args.metadata_json)), args.output)

    if command == "verify_sympy_identity":
        parser.add_argument("--lhs", required=True)
        parser.add_argument("--rhs", required=True)
        parser.add_argument("--vars", required=True)
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        return _json(numerics.verify_sympy_identity(args.lhs, args.rhs, _csv_strings(args.vars)), args.output)

    if command == "finite_difference_check":
        parser.add_argument("--point", type=float, default=1.0)
        parser.add_argument("--expected", type=float)
        parser.add_argument("--step", type=float, default=1e-5)
        parser.add_argument("--tolerance", type=float, default=1e-4)
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        return _json(numerics.finite_difference_report(lambda x: x * x, args.point, args.expected, args.step, args.tolerance), args.output)

    if command == "gradient_check":
        parser.add_argument("--point", default="1,2")
        parser.add_argument("--step", type=float, default=1e-5)
        parser.add_argument("--tolerance", type=float, default=1e-4)
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        point = np.asarray(_csv_numbers(args.point), dtype=float)
        result = numerics.gradient_check(lambda x: float(np.sum(x * x)), lambda x: 2 * x, point, args.step, args.tolerance)
        return _json(result, args.output)

    if command == "search_counterexamples":
        parser.add_argument("--expr", required=True)
        parser.add_argument("--vars", required=True)
        parser.add_argument("--low", type=float, default=-1.0)
        parser.add_argument("--high", type=float, default=1.0)
        parser.add_argument("--trials", type=int, default=1000)
        parser.add_argument("--seed", type=int, default=0)
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        return _json(numerics.search_counterexamples_expression(args.expr, _csv_strings(args.vars), args.low, args.high, args.trials, args.seed), args.output)

    if command == "randomized_property_test":
        parser.add_argument("--expr", required=True, help="Boolean expression over x0, x1, ...")
        parser.add_argument("--dimension", type=int, required=True)
        parser.add_argument("--low", type=float, default=-1.0)
        parser.add_argument("--high", type=float, default=1.0)
        parser.add_argument("--trials", type=int, default=100)
        parser.add_argument("--seed", type=int, default=0)
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        def predicate(sample: np.ndarray) -> bool:
            return bool(evaluate_expression(args.expr, {f"x{i}": float(v) for i, v in enumerate(sample)}))
        return _json(numerics.randomized_property_test(predicate, args.dimension, args.low, args.high, args.trials, args.seed), args.output)

    if command == "stability_sweep":
        parser.add_argument("csv")
        parser.add_argument("--value-column", required=True)
        parser.add_argument("--group-column")
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        df = read_csv_checked(args.csv, [args.value_column])
        groups = df[args.group_column].astype(str).tolist() if args.group_column else None
        return _json(numerics.stability_summary(df[args.value_column].tolist(), groups), args.output)

    if command in {"bootstrap_ci", "permutation_test", "effect_size", "seed_sensitivity"}:
        parser.add_argument("csv")
        parser.add_argument("--value-column", "--metric-column", dest="value_column", required=True)
        parser.add_argument("--group-column")
        parser.add_argument("--seed-column")
        parser.add_argument("--confidence", type=float, default=0.95)
        parser.add_argument("--resamples", type=int, default=1000)
        parser.add_argument("--permutations", type=int, default=1000)
        parser.add_argument("--seed", type=int, default=0)
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        df = read_csv_checked(args.csv, [args.value_column])
        if command == "bootstrap_ci":
            return _json(stats.bootstrap_ci(df[args.value_column], args.confidence, args.resamples, args.seed), args.output)
        if command == "permutation_test":
            _require(args.group_column, "--group-column")
            return _json(stats.permutation_test(df[args.value_column], df[args.group_column], args.permutations, args.seed), args.output)
        if command == "effect_size":
            _require(args.group_column, "--group-column")
            return _json(stats.cohen_d(df[args.value_column], df[args.group_column]), args.output)
        _require(args.seed_column, "--seed-column")
        return _json(stats.seed_sensitivity(df, args.seed_column, args.value_column), args.output)

    if command in {"metric_matrix_audit", "recompute_metric_from_csv", "decompose_metric_contributions"}:
        parser.add_argument("csv")
        parser.add_argument("--row-column", default="row")
        parser.add_argument("--col-column", default="col")
        parser.add_argument("--value-column", default="value")
        parser.add_argument("--expression")
        parser.add_argument("--item-column")
        parser.add_argument("--contribution-column")
        parser.add_argument("--pivot-output")
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        df = pd.read_csv(args.csv)
        if command == "metric_matrix_audit":
            result = metrics.audit_metric_matrix(df, args.row_column, args.col_column, args.value_column)
            if args.pivot_output:
                pd.DataFrame(result["pivot_table"]).to_csv(args.pivot_output)
            return _json(result, args.output)
        if command == "recompute_metric_from_csv":
            _require(args.expression, "--expression")
            return _json(metrics.recompute_metric_from_aggregates(df, args.expression), args.output)
        _require(args.item_column, "--item-column")
        _require(args.contribution_column, "--contribution-column")
        return _json(metrics.decompose_metric_contributions(df, args.item_column, args.contribution_column), args.output)

    if command == "compare_metric_definitions":
        parser.add_argument("definitions_json")
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        return _text(metrics.compare_metric_definitions(load_json(args.definitions_json)), args.output)

    if command in {"check_split_overlap", "hash_duplicates", "config_diff", "result_reproducibility_check"}:
        if command == "check_split_overlap":
            parser.add_argument("--split", action="append", required=True, help="name=path.csv; may repeat")
            parser.add_argument("--key-column", required=True)
            parser.add_argument("--output")
            args = parser.parse_args(argv)
            frames = {name: pd.read_csv(path) for name, path in (item.split("=", 1) for item in args.split)}
            return _json(experiments.check_split_overlap(frames, args.key_column), args.output)
        if command == "hash_duplicates":
            parser.add_argument("paths", nargs="+")
            parser.add_argument("--output")
            args = parser.parse_args(argv)
            return _json(experiments.hash_duplicates(args.paths), args.output)
        if command == "config_diff":
            parser.add_argument("left")
            parser.add_argument("right")
            parser.add_argument("--output")
            args = parser.parse_args(argv)
            return _json(experiments.config_diff(args.left, args.right), args.output)
        parser.add_argument("csv")
        parser.add_argument("--run-column", default="run_id")
        parser.add_argument("--seed-column", default="seed")
        parser.add_argument("--metric-column", default="metric")
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        return _json(experiments.result_reproducibility_check(pd.read_csv(args.csv), args.run_column, args.seed_column, args.metric_column), args.output)

    if command in {"pairwise_distances", "prototype_geometry", "margin_analysis", "embedding_drift"}:
        parser.add_argument("--features")
        parser.add_argument("--labels")
        parser.add_argument("--logits")
        parser.add_argument("--before")
        parser.add_argument("--after")
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        if command == "pairwise_distances":
            _require(args.features, "--features")
            return _json(geometry.pairwise_distance_summary(np.load(args.features)), args.output)
        if command == "prototype_geometry":
            _require(args.features, "--features")
            _require(args.labels, "--labels")
            return _json(geometry.prototype_geometry(np.load(args.features), np.load(args.labels, allow_pickle=True)), args.output)
        if command == "margin_analysis":
            _require(args.logits, "--logits")
            _require(args.labels, "--labels")
            before = np.load(args.before) if args.before else None
            return _json(geometry.margin_analysis(np.load(args.logits), np.load(args.labels), before), args.output)
        _require(args.before, "--before")
        _require(args.after, "--after")
        return _json(geometry.embedding_drift(np.load(args.before), np.load(args.after)), args.output)

    if command in {"svd_energy", "effective_rank", "spectral_entropy", "low_rank_reconstruction"}:
        parser.add_argument("npy")
        parser.add_argument("--rank", type=int, default=1)
        parser.add_argument("--values-are-singular", action="store_true")
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        arr = np.load(args.npy)
        if command == "svd_energy":
            return _json(spectral.svd_energy(arr, args.rank), args.output)
        if command == "effective_rank":
            return _json(spectral.effective_rank(arr, args.values_are_singular), args.output)
        if command == "spectral_entropy":
            return _json(spectral.spectral_entropy(arr, args.values_are_singular), args.output)
        return _json(spectral.low_rank_reconstruction(arr, args.rank), args.output)

    if command in {"loss_curve_audit", "convergence_diagnostics", "gradient_norms", "local_sensitivity"}:
        parser.add_argument("csv")
        parser.add_argument("--step-column", default="step")
        parser.add_argument("--loss-column", default="loss")
        parser.add_argument("--value-column", default="value")
        parser.add_argument("--parameter-column", default="parameter")
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        df = pd.read_csv(args.csv)
        if command == "loss_curve_audit":
            return _json(optimization.loss_curve_audit(df, args.step_column, args.loss_column), args.output)
        if command == "convergence_diagnostics":
            return _json(optimization.convergence_diagnostics(df[args.value_column]), args.output)
        if command == "gradient_norms":
            return _json(optimization.gradient_norm_summary(df[args.value_column]), args.output)
        return _json(optimization.local_sensitivity(df, args.parameter_column, args.value_column), args.output)

    if command in {"pattern_discovery", "hypothesis_graph", "concept_report", "concept_overlap_table", "forbidden_wording_check", "create_concept_record", "update_evidence_table", "concept_status_check"}:
        parser.add_argument("input")
        parser.add_argument("--root", default=".")
        parser.add_argument("--record")
        parser.add_argument("--status")
        parser.add_argument("--evidence-level", type=int)
        parser.add_argument("--literature-validated", action="store_true")
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        if command == "pattern_discovery":
            return _json(concepts.pattern_discovery(pd.read_csv(args.input)), args.output)
        if command == "hypothesis_graph":
            return _text(concepts.hypothesis_graph(load_json(args.input)), args.output)
        if command == "concept_report":
            return _text(concepts.concept_report(load_json(args.input)), args.output)
        if command == "concept_overlap_table":
            return _text(concepts.concept_overlap_table(load_json(args.input)), args.output)
        if command == "forbidden_wording_check":
            data = load_json(args.input)
            return _json(text_tools.forbidden_wording_occurrences(data.get("text", ""), data.get("forbidden", [])), args.output)
        if command == "create_concept_record":
            path = concepts.create_concept_record(load_json(args.input), args.root)
            return _json({"path": str(path)}, args.output)
        if command == "update_evidence_table":
            _require(args.record, "--record")
            path = concepts.update_evidence_table(args.record, load_json(args.input))
            return _json({"path": str(path)}, args.output)
        _require(args.status, "--status")
        _require(args.evidence_level is not None, "--evidence-level")
        return _json(concepts.concept_status_check(args.status, args.evidence_level, args.literature_validated), args.output)

    if command in {"score_research_claim", "build_critique_report", "compare_hypotheses", "rank_next_experiments", "downgrade_ledger", "arbiter_check"}:
        parser.add_argument("input_json")
        parser.add_argument("--output")
        args = parser.parse_args(argv)
        data = load_json(args.input_json)
        if command == "score_research_claim":
            return _json(judge.score_research_claim(data), args.output)
        if command == "build_critique_report":
            return _text(judge.build_critique_report(data), args.output)
        if command == "compare_hypotheses":
            return _json(judge.compare_hypotheses(data), args.output)
        if command == "rank_next_experiments":
            return _json(judge.rank_next_experiments(data.get("experiments", data)), args.output)
        if command == "downgrade_ledger":
            return _text(judge.render_downgrade_ledger(data.get("downgrades", data)), args.output)
        return _json(judge.arbiter_check(data), args.output)

    raise ValueError(f"Unknown script command: {command}")


def _require(value: Any, name: str) -> None:
    if not value:
        raise SystemExit(f"{name} is required")


def _json(data: Any, output: str | None) -> int:
    write_json_output(data, output)
    return 0


def _text(text: str, output: str | None) -> int:
    write_text_output(text, output)
    return 0
