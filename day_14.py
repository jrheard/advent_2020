from collections import defaultdict


def load_input() -> list[str]:
    with open("inputs/day_14.txt") as f:
        return [line.strip() for line in f]


def write_to_memory(
    memory: dict[int, int], address: int, value: int, mask: str
) -> None:
    # The current bitmask is applied to values immediately before they are
    # written to memory: a 0 or 1 overwrites the corresponding bit in the value,
    # while an X leaves the bit in the value unchanged.

    for i, mask_bit in enumerate(reversed(mask)):
        if mask_bit == "1":
            value = value | (1 << i)
        elif mask_bit == "0":
            value = value & ~(1 << i)

    memory[address] = value


def part_1() -> int:
    memory = defaultdict(int)
    mask = ""

    for line in load_input():
        if line.startswith("mask"):
            mask = line[7:]
        else:
            address = int(line[4 : line.find("]")])
            value = int(line.split(" = ")[1])
            write_to_memory(memory, address, value, mask)

    # Execute the initialization program. What is the sum of all values left in
    # memory after it completes? (Do not truncate the sum to 36 bits.)
    return sum(memory.values())


def part_2() -> int:
    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
