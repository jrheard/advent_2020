def load_input() -> list[tuple[str, int]]:
    with open("inputs/day_8.txt") as f:
        lines = [line.strip().split(" ") for line in f]

    return [(instruction, int(value)) for instruction, value in lines]


def part_1() -> int:
    instructions = load_input()

    instruction_pointer = 0
    visited_instructions = set()
    accumulator = 0

    # Immediately before any instruction is executed a second time, what value is in the accumulator?
    while True:
        match instructions[instruction_pointer]:
            case ["acc", num]:
                accumulator += num
                instruction_pointer += 1
            case ["jmp", num]:
                instruction_pointer += num
                if instruction_pointer in visited_instructions:
                    # We've visited this instruction before - time to return the accumulator!
                    break
            case ["nop", _]:
                instruction_pointer += 1

        visited_instructions.add(instruction_pointer)

    return accumulator


def part_2() -> int:
    return 1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
