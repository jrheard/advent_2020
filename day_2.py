import re


INPUT_RE = re.compile(r"(\d+)-(\d+) (\w): (\w+)")


def is_password_valid_part_1(input_line: str) -> bool:
    min_occurrences, max_occurrences, char, password = re.match(
        INPUT_RE, input_line
    ).groups()
    min_occurrences = int(min_occurrences)
    max_occurrences = int(max_occurrences)

    return min_occurrences <= password.count(char) <= max_occurrences


# Each line gives the password policy and then the password. The password policy
# indicates the lowest and highest number of times a given letter must appear
# for the password to be valid. For example, 1-3 a means that the password must
# contain a at least 1 time and at most 3 times.
def part_1() -> int:
    with open("inputs/day_2.txt") as f:
        lines = [line.strip() for line in f]

    return sum(is_password_valid_part_1(line) for line in lines)


def is_password_valid_part_2(input_line: str) -> bool:
    index_1, index_2, char, password = re.match(INPUT_RE, input_line).groups()

    char_1 = password[int(index_1) - 1]
    char_2 = password[int(index_2) - 1]

    if char_1 == char_2:
        return False

    return char_1 == char or char_2 == char


def part_2() -> int:
    with open("inputs/day_2.txt") as f:
        lines = [line.strip() for line in f]

    return sum(is_password_valid_part_2(line) for line in lines)


if __name__ == "__main__":
    print(part_2())
