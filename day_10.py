import itertools


def load_input() -> list[int]:
    with open("inputs/day_10.txt") as f:
        file_joltages = list(sorted(int(line.strip()) for line in f))

    # Treat the charging outlet near your seat as having an effective joltage rating of 0.
    return [0] + file_joltages


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


def num_available_adapters(adapter_joltages: list[int]) -> int:
    return sum(
        1 for joltage in adapter_joltages[1:4] if adapter_joltages[0] - joltage <= 3
    )


def part_2() -> int:
    joltages = sorted(load_input(), reverse=True)

    num_permutations = 1

    while joltages != [0]:
        num_available = num_available_adapters(joltages)
        num_permutations *= num_available
        joltages = joltages[num_available:]

    return num_permutations


if __name__ == "__main__":
    print(part_1())
    print(part_2())
