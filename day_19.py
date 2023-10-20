from typing import Iterator


def load_input() -> tuple[dict[str, str], list[str]]:
    with open("inputs/day_19.txt") as f:
        lines = [line.strip() for line in f]

    delimiter_index = lines.index("")
    rules = {
        line.split(": ")[0]: line.split(": ")[1] for line in lines[:delimiter_index]
    }

    return rules, lines[delimiter_index + 1 :]


def expand_rule_string(
    rule_string: str, rules: dict[str, str], leaf_rules: set[str]
) -> Iterator[str]:
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


# The instructions said that we should handle our specific list of rules directly rather than
# try to make a formal grammar, so that's what I'm going to do. This function relies on specific
# knowledge of our rules 0, 8, 11, 42, and 31:
# 0: 8 11
# 8: 42 | 42 8
# 11: 42 31 | 42 11 31
# Rules 8 and 11 can loop indefinitely. Rules 42, 31, and all other rules downstream from them cannot loop.
def does_string_match_part_2(
    string: str, rule_31_strings: set[str], rule_42_strings: set[str]
) -> bool:
    if len(string) % 8 != 0:
        return False

    for rule_8_part, rule_11_part in split_string_into_two_chunks_8_chars_at_a_time(
        string
    ):
        if does_string_match_rule_8(
            rule_8_part, rule_42_strings
        ) and does_string_match_rule_11(rule_11_part, rule_31_strings, rule_42_strings):
            return True

    return False


# 8: 42 | 42 8
def does_string_match_rule_8(string: str, rule_42_strings: set[str]) -> bool:
    for chunk in split_string_into_chunks_of_8_chars(string):
        if chunk not in rule_42_strings:
            return False
    return True


# 11: 42 31 | 42 11 31
def does_string_match_rule_11(
    string: str, rule_31_strings: set[str], rule_42_strings: set[str]
) -> bool:
    chunks = split_string_into_chunks_of_8_chars(string)
    if chunks[0] not in rule_42_strings or chunks[-1] not in rule_31_strings:
        return False

    if len(chunks) == 2:
        return True

    return does_string_match_rule_11(
        "".join(chunks[1:-1]), rule_31_strings, rule_42_strings
    )


def split_string_into_two_chunks_8_chars_at_a_time(
    string: str,
) -> Iterator[list[str]]:
    assert len(string) % 8 == 0

    for i in range(0, len(string), 8)[:-1]:
        yield [string[:i], string[i:]]


def split_string_into_chunks_of_8_chars(string) -> list[str]:
    assert len(string) % 8 == 0

    result = []
    for i in range(0, len(string), 8):
        result.append(string[i : i + 8])

    return result


def part_1() -> int:
    rules, strings = load_input()
    leaf_rules = {
        rule_key for rule_key, rule_value in rules.items() if rule_value.startswith('"')
    }
    valid_strings = set(expand_rule_string("0", rules, leaf_rules))
    return sum(1 for string in strings if string in valid_strings)


def part_2() -> int:
    rules, strings = load_input()
    leaf_rules = {
        rule_key for rule_key, rule_value in rules.items() if rule_value.startswith('"')
    }
    rule_31_strings = set(expand_rule_string("31", rules, leaf_rules))
    rule_42_strings = set(expand_rule_string("42", rules, leaf_rules))
    return sum(
        1
        for string in strings
        if does_string_match_part_2(string, rule_31_strings, rule_42_strings)
    )


if __name__ == "__main__":
    # print(part_1())
    print(part_2())
