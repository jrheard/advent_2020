import collections
import itertools


def load_input() -> list[int]:
    with open("inputs/day_9.txt") as f:
        return [int(line.strip()) for line in f]


def can_number_be_constructed_from_any_pair_of_numbers(
    number: int, candidates: collections.deque[int]
) -> bool:
    for i, num_1 in enumerate(candidates):
        for num_2 in itertools.islice(candidates, i + 1, len(candidates)):
            if num_1 + num_2 == number:
                return True

    return False


def part_1() -> int:
    # The first step of attacking the weakness in the XMAS data is to find the
    # first number in the list (after the preamble) which is not the sum of two
    # of the 25 numbers before it. What is the first number that does not have
    # this property?
    xmas_data = load_input()
    previous_25_numbers = collections.deque(xmas_data[:25])
    for number in xmas_data[25:]:
        if not can_number_be_constructed_from_any_pair_of_numbers(
            number, previous_25_numbers
        ):
            return number

        previous_25_numbers.popleft()
        previous_25_numbers.append(number)

    return -1


def part_2() -> int:
    # The final step in breaking the XMAS encryption relies on the invalid
    # number you just found: you must find a contiguous set of at least two
    # numbers in your list which sum to the invalid number from step 1.
    target_number = part_1()

    xmas_data = load_input()
    for i in range(len(xmas_data)):
        for j in range(len(xmas_data) - i):
            contiguous_numbers = xmas_data[i : i + j]
            if sum(contiguous_numbers) == target_number:
                return min(contiguous_numbers) + max(contiguous_numbers)

    return 1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
