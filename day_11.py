from enum import Enum, auto
from dataclasses import dataclass
import itertools

# Day 11's looking like game of life; I've implemented that before
# and have found a noticeable perf improvement from storing the grid
# as an encapsulated 1d list rather than as a directly-accessed 2d list,
# so that's the approach I'll go with here.


class GridValue(Enum):
    EMPTY_SEAT = "L"
    OCCUPIED_SEAT = "#"
    FLOOR = "."


@dataclass(frozen=True)
class SeatGrid:
    seats: tuple[GridValue]
    width: int
    height: int

    def value_at(self, x: int, y: int) -> GridValue:
        return self.seats[y * self.width + x]

    def num_occupied_neighbors(self, x: int, y: int) -> int:
        neighbor_coordinates = [
            (xx, yy)
            for xx, yy in itertools.product(range(x - 1, x + 2), range(y - 1, y + 2))
            if 0 <= xx < self.width and 0 <= yy < self.height
        ]

        return sum(
            1
            for (x, y) in neighbor_coordinates
            if self.value_at(x, y) == GridValue.OCCUPIED_SEAT
        )


def load_input() -> SeatGrid:
    with open("inputs/day_11.txt") as f:
        lines = [line.strip() for line in f]

    return SeatGrid(
        seats=tuple(GridValue(char) for char in "".join(lines)),
        width=len(lines[0]),
        height=len(lines),
    )


def part_1() -> int:
    grid = load_input()
    breakpoint()
    return -1


def part_2() -> int:
    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
