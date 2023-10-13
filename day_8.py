Instruction = tuple[str, int]


def load_input() -> list[Instruction]:
    with open("inputs/day_8.txt") as f:
        lines = [line.strip().split(" ") for line in f]

    return [(instruction, int(value)) for instruction, value in lines]


def does_program_contain_an_infinite_loop(
    instructions: list[Instruction],
) -> tuple[bool, int]:
    instruction_pointer = 0
    visited_instructions = set()
    accumulator = 0

    while True:
        if instruction_pointer == len(instructions):
            return False, accumulator

        match instructions[instruction_pointer]:
            case ["acc", num]:
                accumulator += num
                instruction_pointer += 1
            case ["jmp", num]:
                instruction_pointer += num
                if instruction_pointer in visited_instructions:
                    # We've visited this instruction before - the program contains an infinite loop!
                    return True, accumulator
            case ["nop", _]:
                instruction_pointer += 1

        visited_instructions.add(instruction_pointer)


def part_1() -> int:
    # Immediately before any instruction is executed a second time, what value is in the accumulator?
    return does_program_contain_an_infinite_loop(load_input())[1]


def part_2() -> int:
    return 1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
