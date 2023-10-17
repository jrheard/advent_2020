from collections import defaultdict


def load_input() -> list[str]:
    with open("inputs/day_14.txt") as f:
        return [line.strip() for line in f]


def write_to_memory_applying_mask_to_value(
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


def compute_target_addresses(
    address: int, floating_bit_indexes: list[int]
) -> list[int]:
    if not floating_bit_indexes:
        return [address]

    address_with_first_floating_bit_set_to_0 = address & ~(1 << floating_bit_indexes[0])
    address_with_first_floating_bit_set_to_1 = address | (1 << floating_bit_indexes[0])
    return compute_target_addresses(
        address_with_first_floating_bit_set_to_0, floating_bit_indexes[1:]
    ) + compute_target_addresses(
        address_with_first_floating_bit_set_to_1, floating_bit_indexes[1:]
    )


def write_to_memory_applying_mask_to_address(
    memory: dict[int, int], address: int, value: int, mask: str
) -> None:
    # Immediately before a value is written to memory, each bit in the bitmask modifies the corresponding bit of the destination memory address in the following way:
    # If the bitmask bit is 0, the corresponding memory address bit is unchanged.
    # If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
    # If the bitmask bit is X, the corresponding memory address bit is floating.

    for i, mask_bit in enumerate(reversed(mask)):
        if mask_bit == "1":
            address = address | (1 << i)

    floating_bit_indexes = [
        i for i, mask_bit in enumerate(reversed(mask)) if mask_bit == "X"
    ]

    for target_address in compute_target_addresses(address, floating_bit_indexes):
        memory[target_address] = value


def run_program_with_write_fn(write_fn) -> int:
    memory = defaultdict(int)
    mask = ""

    for line in load_input():
        if line.startswith("mask"):
            mask = line[7:]
        else:
            address = int(line[4 : line.find("]")])
            value = int(line.split(" = ")[1])
            write_fn(memory, address, value, mask)

    # Execute the initialization program. What is the sum of all values left in
    # memory after it completes? (Do not truncate the sum to 36 bits.)
    return sum(memory.values())


def part_1() -> int:
    return run_program_with_write_fn(write_to_memory_applying_mask_to_value)


def part_2() -> int:
    return run_program_with_write_fn(write_to_memory_applying_mask_to_address)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
