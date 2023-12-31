from __future__ import annotations
from dataclasses import dataclass
from typing import Literal


@dataclass
class Expression:
    left: int | Expression
    right: Expression | None
    operator: str | None
    parentheses_depth: int


def parse_expression_string(
    expression_string: str, parentheses_depth: int
) -> Expression:
    if expression_string[0] == "(":
        closing_paren_index = find_position_of_matching_closing_parenthesis(
            expression_string
        )
        left = parse_expression_string(
            expression_string[1:closing_paren_index], parentheses_depth + 1
        )

        if closing_paren_index != len(expression_string) - 1:
            operator_index = closing_paren_index + 2
        else:
            operator_index = None

    else:
        left = int(expression_string[0])
        operator_index = 2 if len(expression_string) > 1 else None

    return Expression(
        left,
        parse_expression_string(
            expression_string[operator_index + 2 :], parentheses_depth
        )
        if operator_index
        else None,
        expression_string[operator_index] if operator_index else None,
        parentheses_depth,
    )


def evaluate_leaf_expression(expression: Expression) -> int:
    assert isinstance(expression.left, int)
    result = expression.left

    if expression.right is None:
        return result

    while expression is not None:
        operator = expression.operator
        assert isinstance(expression.right, Expression)
        assert isinstance(expression.right.left, int)

        if operator == "+":
            result += expression.right.left
        else:
            result *= expression.right.left

        expression = expression.right
        if expression.right is None:
            break

    return result


def collapse_arithmetic_expressions(expression: Expression) -> None:
    while expression.right is not None:
        if expression.operator == "+":
            assert isinstance(expression.left, int)
            assert isinstance(expression.right.left, int)
            expression.left += expression.right.left

            expression.operator = expression.right.operator
            expression.right = expression.right.right

        else:
            expression = expression.right


def find_largest_parentheses_depth_in_expression(expression: Expression) -> int:
    candidates = [expression.parentheses_depth]
    if isinstance(expression.left, Expression):
        candidates.append(find_largest_parentheses_depth_in_expression(expression.left))
    if isinstance(expression.right, Expression):
        candidates.append(
            find_largest_parentheses_depth_in_expression(expression.right)
        )

    return max(candidates)


def find_parent_of_expression_with_depth(
    expression: Expression, depth: int
) -> tuple[Expression, Literal["left", "right"]] | None:
    if isinstance(expression.left, Expression):
        if expression.left.parentheses_depth == depth:
            return (expression, "left")
        elif (
            left_result := find_parent_of_expression_with_depth(expression.left, depth)
        ) is not None:
            return left_result

    if isinstance(expression.right, Expression):
        if expression.right.parentheses_depth == depth:
            return (expression, "right")
        elif (
            right_result := find_parent_of_expression_with_depth(
                expression.right, depth
            )
        ) is not None:
            return right_result


def replace_parenthesized_expressions_with_ints(
    expression: Expression, evaluate_leaf_expression_fn
) -> None:
    largest_depth = find_largest_parentheses_depth_in_expression(expression)
    if largest_depth == 0:
        # If there are no nested parenthesized expressions, we're done!
        return

    parent_info = find_parent_of_expression_with_depth(expression, largest_depth)
    assert parent_info is not None

    parent, direction = parent_info
    if direction == "left":
        assert isinstance(parent.left, Expression)
        parent.left = evaluate_leaf_expression_fn(parent.left)
    else:
        assert isinstance(parent.right, Expression)
        parent.right = Expression(
            evaluate_leaf_expression_fn(parent.right),
            None,
            None,
            0,
        )

    # Recur to replace the next-deepest parenthesized expression.
    replace_parenthesized_expressions_with_ints(expression, evaluate_leaf_expression_fn)


def load_input() -> list[str]:
    with open("inputs/day_18.txt") as f:
        return [line.strip() for line in f]


def find_position_of_matching_closing_parenthesis(string: str) -> int:
    if string[0] != "(":
        raise ValueError(
            f"Expected first character of {string} to be an open parenthesis"
        )

    num_open_parentheses_seen = 1
    for i, char in enumerate(string[1:]):
        if char == "(":
            num_open_parentheses_seen += 1
        elif char == ")":
            if num_open_parentheses_seen == 1:
                return i + 1
            else:
                num_open_parentheses_seen -= 1

    return -1


def evaluate_expression_string(expression_string: str) -> int:
    expr = parse_expression_string(expression_string, 0)
    replace_parenthesized_expressions_with_ints(expr, evaluate_leaf_expression)
    return evaluate_leaf_expression(expr)


def part_1() -> int:
    # Before you can help with the homework, you need to understand it yourself.
    # Evaluate the expression on each line of the homework; what is the sum of
    # the resulting values?
    values = (
        evaluate_expression_string(expression_string)
        for expression_string in load_input()
    )
    return sum(values)


def evaluate_leaf_expression_prioritizing_addition(expression: Expression) -> int:
    collapse_arithmetic_expressions(expression)
    return evaluate_leaf_expression(expression)


def evaluate_expression_string_prioritizing_addition(expression_string: str) -> int:
    expr = parse_expression_string(expression_string, 0)
    replace_parenthesized_expressions_with_ints(
        expr, evaluate_leaf_expression_prioritizing_addition
    )
    return evaluate_leaf_expression_prioritizing_addition(expr)


def part_2() -> int:
    # Now, addition and multiplication have different precedence levels, but
    # they're not the ones you're familiar with. Instead, addition is evaluated before multiplication.
    # What do you get if you add up the results of evaluating the homework problems using these new rules?
    values = (
        evaluate_expression_string_prioritizing_addition(expression_string)
        for expression_string in load_input()
    )
    return sum(values)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
