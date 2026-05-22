from __future__ import annotations

import ast
import math
import operator
from typing import Any, Mapping


_ALLOWED_FUNCS = {
    "abs": abs,
    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "min": min,
    "max": max,
}

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg, ast.Not: operator.not_}

_COMPARE_OPS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
}


class UnsafeExpressionError(ValueError):
    '''Raised when an expression uses unsupported or unsafe syntax.'''


def evaluate_expression(expression: str, variables: Mapping[str, Any]) -> Any:
    '''Evaluate a restricted arithmetic/boolean expression over provided variables.'''
    tree = ast.parse(expression, mode="eval")
    return _eval_node(tree.body, variables)


def _eval_node(node: ast.AST, variables: Mapping[str, Any]) -> Any:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, bool)):
        return node.value
    if isinstance(node, ast.Name):
        if node.id not in variables:
            raise UnsafeExpressionError(f"Unknown variable: {node.id}")
        return variables[node.id]
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        return _BIN_OPS[type(node.op)](_eval_node(node.left, variables), _eval_node(node.right, variables))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval_node(node.operand, variables))
    if isinstance(node, ast.BoolOp):
        values = [_eval_node(v, variables) for v in node.values]
        if isinstance(node.op, ast.And):
            return all(values)
        if isinstance(node.op, ast.Or):
            return any(values)
    if isinstance(node, ast.Compare):
        left = _eval_node(node.left, variables)
        for op, comparator in zip(node.ops, node.comparators):
            if type(op) not in _COMPARE_OPS:
                raise UnsafeExpressionError(f"Unsupported comparison: {type(op).__name__}")
            right = _eval_node(comparator, variables)
            if not _COMPARE_OPS[type(op)](left, right):
                return False
            left = right
        return True
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id not in _ALLOWED_FUNCS:
            raise UnsafeExpressionError(f"Unsupported function: {node.func.id}")
        args = [_eval_node(arg, variables) for arg in node.args]
        if node.keywords:
            raise UnsafeExpressionError("Keyword arguments are not supported")
        return _ALLOWED_FUNCS[node.func.id](*args)
    raise UnsafeExpressionError(f"Unsupported expression syntax: {type(node).__name__}")
