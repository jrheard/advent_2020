def load_input(filename: str) -> list[str]:
    with open(f"inputs/{filename}") as f:
        return [line.strip() for line in f]


# Before you leave, the Elves in accounting just need you to fix your expense
# report (your puzzle input); apparently, something isn't quite adding up.
#
# Specifically, they need you to find the two entries that sum to 2020 and then
# multiply those two numbers together.
def part_1() -> int:
    numbers = [int(line) for line in load_input("day_1.txt")]

    for i, num_1 in enumerate(numbers):
        for num_2 in numbers[i + 1 :]:
            if num_1 + num_2 == 2020:
                return num_1 * num_2

    return -1


# The Elves in accounting are thankful for your help; one of them even offers
# you a starfish coin they had left over from a past vacation. They offer you a
# second one if you can find three numbers in your expense report that meet the
# same criteria.
#
# In your expense report, what is the product of the three entries that sum to 2020?
def part_2() -> int:
    numbers = [int(line) for line in load_input("day_1.txt")]

    for i, num_1 in enumerate(numbers):
        for j, num_2 in enumerate(numbers[i + 1 :]):
            for num_3 in numbers[j + 1 :]:
                if num_1 + num_2 + num_3 == 2020:
                    return num_1 * num_2 * num_3

    return -1
