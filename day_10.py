from functools import lru_cache
import itertools


def load_input() -> tuple[int]:
    with open("inputs/day_10.txt") as f:
        file_joltages = tuple(sorted(int(line.strip()) for line in f))

    # Treat the charging outlet near your seat as having an effective joltage rating of 0.
    return (0,) + file_joltages


def part_1() -> int:
    adapter_joltages = load_input()

    # Find a chain that uses all of your adapters to connect the charging outlet
    # to your device's built-in adapter and count the joltage differences
    # between the charging outlet, the adapters, and your device.
    # What is the number of 1-jolt differences multiplied by the number of 3-jolt differences?
    usages_per_joltage_difference = {1: 0, 2: 0, 3: 0}

    for i, joltage in enumerate(adapter_joltages):
        if i < len(adapter_joltages) - 1:
            joltage_difference = adapter_joltages[i + 1] - joltage
            usages_per_joltage_difference[joltage_difference] += 1

    # Your device has a built-in joltage adapter rated for 3 jolts higher than
    # the highest-rated adapter in your bag. (If your adapter list were 3, 9,
    # and 6, your device's built-in adapter would be rated for 12 jolts.)
    usages_per_joltage_difference[3] += 1

    return usages_per_joltage_difference[1] * usages_per_joltage_difference[3]


def num_available_adapters(adapter_joltages: tuple[int]) -> int:
    return sum(
        1 for joltage in adapter_joltages[1:4] if joltage - adapter_joltages[0] <= 3
    )


@lru_cache()
def num_permutations_of_adapters(joltages: tuple[int]) -> int:
    if len(joltages) == 1:
        return 1

    if num_available_adapters(joltages) == 1:
        return num_permutations_of_adapters(joltages[1:])

    num_available = num_available_adapters(joltages)
    return sum(
        num_permutations_of_adapters(joltages[i:]) for i in range(1, num_available + 1)
    )


def part_2() -> int:
    # this one kicked my ass, gave up after spinning my wheels for a couple days,
    # going with https://0xdf.gitlab.io/adventofcode2020/10's approach
    # i was close but just didn't quite get there! oh well
    return num_permutations_of_adapters(load_input())


if __name__ == "__main__":
    print(part_1())
    print(part_2())
