import re


INPUT_RE = re.compile("(\d+)-(\d+) (\w): (\w+)")


def is_password_valid(input_line: str) -> bool:
    min_occurrences, max_occurrences, char, password = re.match(
        INPUT_RE, input_line
    ).groups()
    min_occurrences = int(min_occurrences)
    max_occurrences = int(max_occurrences)

    return min_occurrences <= password.count(char) <= max_occurrences


def part_1() -> int:
    # i know, i'll use a regular expression!
    with open("inputs/day_2.txt") as f:
        lines = [line.strip() for line in f]

    return sum(is_password_valid(line) for line in lines)


def part_2() -> int:
    pass


if __name__ == "__main__":
    print(part_1())
