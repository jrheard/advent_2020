def load_input() -> list[set[str]]:
    with open("inputs/day_6.txt") as f:
        lines = [line.strip() for line in f]

    group_answers = []
    group_answers_in_progress = set()

    for line in lines:
        if line == "":
            group_answers.append(group_answers_in_progress)
            group_answers_in_progress = set()

        else:
            group_answers_in_progress |= set(line)

    if group_answers_in_progress:
        group_answers.append(group_answers_in_progress)

    return group_answers


def part_1() -> int:
    # For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?
    group_answers = load_input()
    return sum(map(len, group_answers))


def part_2() -> int:
    return 1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
