from typing import Iterator


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


def part_1() -> int:
    rules, strings = load_input()
    return sum(1 for string in strings if does_string_match_rule(string, "0", rules))


def part_2() -> int:
    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
