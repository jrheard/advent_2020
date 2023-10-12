NUM_ROWS_ON_PLANE = 128
NUM_COLUMNS_ON_PLANE = 8


def load_boarding_passes() -> list[str]:
    with open("inputs/day_5.txt") as f:
        return [line.strip() for line in f]


def parse_boarding_pass(boarding_pass: str) -> tuple[int, int]:
    row_range = [0, NUM_ROWS_ON_PLANE - 1]
    for char in boarding_pass[:7]:
        half_row_range_difference = (row_range[1] - row_range[0]) // 2 + 1
        if char == "F":
            row_range[1] -= half_row_range_difference
        else:
            row_range[0] += half_row_range_difference

    col_range = [0, NUM_COLUMNS_ON_PLANE - 1]
    for char in boarding_pass[7:]:
        half_col_range_difference = (col_range[1] - col_range[0]) // 2 + 1
        if char == "L":
            col_range[1] -= half_col_range_difference
        else:
            col_range[0] += half_col_range_difference

    assert row_range[0] == row_range[1]
    assert col_range[0] == col_range[1]

    return row_range[0], col_range[0]


def part_1() -> int:
    # Every seat also has a unique seat ID: multiply the row by 8, then add the column.
    # As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?
    return max(
        row * 8 + col for row, col in map(parse_boarding_pass, load_boarding_passes())
    )


def part_2() -> int:
    pass


if __name__ == "__main__":
    print(part_1())
    print(part_2())
