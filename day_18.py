from __future__ import annotations
from dataclasses import dataclass
from typing import Literal


@dataclass
class Expression:
    left: int | Expression
    right: int | Expression | None
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
    result = 0 if expression.operator == "+" else 1
    operator = expression.operator
    while True:
        assert isinstance(expression.left, int)

        if operator == "+":
            result += expression.left
        else:
            result *= expression.left

        if expression.right is None:
            break

        assert isinstance(expression.right, Expression)
        expression = expression.right

    return result


def find_parent_of_deepest_parenthesized_expression(
    expression,
) -> tuple[Expression, Literal["left", "right"]] | None:
    parent = expression
    max_depth = 0
    # TODO

    pass


def replace_parenthesized_expressions_with_ints(expression: Expression) -> None:
    parent_info = find_parent_of_deepest_parenthesized_expression(expression)

    if not parent_info:
        # If there are no nested parenthesized expressions, we're done!
        return

    parent, direction = parent_info
    if direction == "left":
        assert isinstance(parent.left, Expression)
        parent.left = evaluate_leaf_expression(parent.left)
    else:
        assert isinstance(parent.right, Expression)
        parent.right = evaluate_leaf_expression(parent.right)

    # Recur to replace the next-deepest parenthesized expression.
    replace_parenthesized_expressions_with_ints(expression)


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


def part_1() -> int:
    print(parse_expression_string("2 * 3 + (4 * 5)", 0))
    print(
        evaluate_leaf_expression(
            Expression(
                left=4,
                right=Expression(
                    left=5, right=None, operator=None, parentheses_depth=1
                ),
                operator="*",
                parentheses_depth=1,
            )
        )
    )
    print(parse_expression_string("2 * 3 + (4 * 5)", 0))
    return -1


def part_2() -> int:
    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
