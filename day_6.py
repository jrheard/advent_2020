import functools

from util import load_line_groups_from_file


def part_1() -> int:
    # For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?
    unprocessed_group_answers = load_line_groups_from_file("inputs/day_6.txt")
    processed_group_answers = [
        functools.reduce(lambda x, y: x | set(y), group_answers, set())
        for group_answers in unprocessed_group_answers
    ]

    return sum(map(len, processed_group_answers))


def part_2() -> int:
    return 1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
