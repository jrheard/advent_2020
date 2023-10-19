from typing import Any, Iterator


def load_input() -> tuple[dict[str, str], list[str]]:
    with open("inputs/day_19.txt") as f:
        lines = [line.strip() for line in f]

    delimiter_index = lines.index("")
    rules = {
        line.split(": ")[0]: line.split(": ")[1] for line in lines[:delimiter_index]
    }

    return rules, lines[delimiter_index + 1 :]


def split_string_into_all_possible_chunks(
    string: str, num_chunks: int
) -> Iterator[list[str]]:
    assert num_chunks in (2, 3)

    if num_chunks == 2:
        for i in range(1, len(string)):
            yield [string[:i], string[i:]]
    else:
        for i in range(1, len(string) - 1):
            for j in range(i + 1, len(string)):
                yield [string[:i], string[i:j], string[j:]]


def does_string_match_rule(string: str, rule_key: str, rules: dict[str, str]) -> bool:
    if len(sub_rules := rule_key.split(" ")) > 1:
        # `rule_key` looks like "4 1 5" or "2 8".

        for chunked_string in split_string_into_all_possible_chunks(
            string, len(sub_rules)
        ):
            if all(
                does_string_match_rule(chunk, sub_rule, rules)
                for chunk, sub_rule in zip(chunked_string, sub_rules)
            ):
                return True

        return False

    rule_value = rules[rule_key]
    if rule_value.startswith('"'):
        # This is a leaf rule, with a value like "a" or "b".
        return string == rule_value[1]

    if len(candidates := rule_value.split(" | ")) > 1:
        # The rule's value looks like `10 4 | 2 8 | 6`.
        return any(
            does_string_match_rule(string, candidate, rules) for candidate in candidates
        )

    return does_string_match_rule(string, rule_value, rules)


def expand_rule_string(
    rule_string: str, rules: dict[str, str], leaf_rules: set[str]
) -> Iterator[str]:
    # print(f"expanding {rule_string=}")
    for possible_rule_string in rule_string.split(" | "):
        sub_rules = possible_rule_string.split(" ")
        if all(sub_rule in leaf_rules for sub_rule in sub_rules):
            # possible_rule_string is a series of leaf rules (like "4" or "4 5"), yield their value (like "a" or "ab")
            yield "".join(rules[sub_rule][1] for sub_rule in sub_rules)

        elif all(sub_rule not in leaf_rules for sub_rule in sub_rules):
            # possible_rule_string is a series of non-leaf rules, expand them.

            if len(sub_rules) == 1:
                for string in expand_rule_string(
                    rules[possible_rule_string], rules, leaf_rules
                ):
                    yield string
            else:
                for string_1 in expand_rule_string(
                    rules[sub_rules[0]], rules, leaf_rules
                ):
                    for string_2 in expand_rule_string(
                        rules[sub_rules[1]], rules, leaf_rules
                    ):
                        yield f"{string_1}{string_2}"

        # At this point, we know we have a mixture of leaf and non-leaf rules in possible_rule_string.
        elif len(sub_rules) == 3:
            # Only one of the inputs is shaped like this, the example input rule "0" with value "4 1 5".
            # That rule contains a leaf, non-leaf, and leaf rule in that order.
            # I'm fine with special-casing it because all of the other sub_rule lists will always be of length 2.
            for string in expand_rule_string(sub_rules[1], rules, leaf_rules):
                yield f"{rules[sub_rules[0]][1]}{string}{rules[sub_rules[2]][1]}"

        else:
            assert len(sub_rules) == 2
            if sub_rules[0] in leaf_rules:
                for string in expand_rule_string(sub_rules[1], rules, leaf_rules):
                    yield f"{rules[sub_rules[0]][1]}{string}"
            else:
                for string in expand_rule_string(sub_rules[0], rules, leaf_rules):
                    yield f"{string}{rules[sub_rules[1]][1]}"


def part_1() -> int:
    rules, strings = load_input()
    leaf_rules = {
        rule_key for rule_key, rule_value in rules.items() if rule_value.startswith('"')
    }
    valid_strings = set(expand_rule_string("0", rules, leaf_rules))
    return sum(1 for string in strings if string in valid_strings)


def part_2() -> int:
    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
