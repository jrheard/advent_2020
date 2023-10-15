from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from functools import lru_cache
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
            if 0 <= xx < self.width and 0 <= yy < self.height and (xx, yy) != (x, y)
        ]

        return sum(
            1
            for (xx, yy) in neighbor_coordinates
            if self.value_at(xx, yy) == GridValue.OCCUPIED_SEAT
        )

    def one_round_later(self) -> SeatGrid:
        # The following rules are applied to every seat simultaneously:
        new_seat_values = []

        for y in range(0, self.height):
            for x in range(0, self.width):
                value = self.value_at(x, y)

                if (
                    value == GridValue.EMPTY_SEAT
                    and self.num_occupied_neighbors(x, y) == 0
                ):
                    # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
                    new_value = GridValue.OCCUPIED_SEAT
                elif (
                    value == GridValue.OCCUPIED_SEAT
                    and self.num_occupied_neighbors(x, y) >= 4
                ):
                    # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
                    new_value = GridValue.EMPTY_SEAT
                else:
                    # Otherwise, the seat's state does not change.
                    new_value = value

                if new_value == GridValue.FLOOR and value != GridValue.FLOOR:
                    breakpoint()
                new_seat_values.append(new_value)

        return SeatGrid(
            seats=tuple(new_seat_values), width=self.width, height=self.height
        )

    def print(self) -> None:
        for i, seat in enumerate(self.seats):
            if i % 10 == 0:
                print()
            print(seat.value, end="")
        print()


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

    # Simulate your seating area by applying the seating rules repeatedly until no seats change state.
    # How many seats end up occupied?
    while True:
        next_grid = grid.one_round_later()

        if grid == next_grid:
            break

        grid = next_grid

    return sum(1 for seat in grid.seats if seat == GridValue.OCCUPIED_SEAT)


def part_2() -> int:
    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
