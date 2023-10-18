from __future__ import annotations
from dataclasses import dataclass


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

        expression = expression.right

    return result


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


def evaluate_parenthesized_expression(expression: str) -> int:
    closing_paren_index = find_position_of_matching_closing_parenthesis(expression)
    leftmost_value = evaluate_expression(expression[1:closing_paren_index])

    if closing_paren_index == len(expression) - 1:
        return leftmost_value

    operator = expression[closing_paren_index + 2]
    rest_of_expression = expression[closing_paren_index + 4 :]


def evaluate_expression(expression: str) -> int:
    # "However, the rules of operator precedence have changed. Rather than
    # evaluating multiplication before addition, the operators have the same
    # precedence, and are evaluated left-to-right regardless of the order in
    # which they appear."

    if expression[0] == "(":
        closing_paren_index = find_position_of_matching_closing_parenthesis(expression)
        leftmost_value = evaluate_expression(expression[1:closing_paren_index])

        if closing_paren_index == len(expression) - 1:
            return leftmost_value

        operator = expression[closing_paren_index + 2]
        rest_of_expression = expression[closing_paren_index + 4 :]

    else:
        leftmost_value = int(expression[0])

        if len(expression) == 1:
            return leftmost_value

        operator = expression[2]
        rest_of_expression = expression[4:]

    if operator == "+":
        print(
            f"{expression=}, {rest_of_expression=}, {leftmost_value=} + {evaluate_expression(rest_of_expression)=}"
        )
        return leftmost_value + evaluate_expression(rest_of_expression)
    else:
        print(
            f"{expression=}, {rest_of_expression=}, {leftmost_value=} * {evaluate_expression(rest_of_expression)=}"
        )
        return leftmost_value * evaluate_expression(rest_of_expression)


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
