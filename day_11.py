from __future__ import annotations

from enum import Enum, auto
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


class WhichNeighborAlgorithmToUse(Enum):
    IMMEDIATELY_ADJACENT = auto()
    LINE_OF_SIGHT = auto()


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

    def value_of_first_visible_seat_in_direction(
        self, x: int, y: int, direction: tuple[int, int]
    ) -> GridValue:
        x_delta, y_delta = direction

        while True:
            if not (0 <= x + x_delta < self.width) or not (
                0 <= y + y_delta < self.height
            ):
                # Didn't find any seats in this direction, occupied or otherwise.
                return GridValue.FLOOR

            if (value := self.value_at(x + x_delta, y + y_delta)) != GridValue.FLOOR:
                # Found a seat!
                return value

            x_delta += direction[0]
            y_delta += direction[1]

    def num_occupied_neighbors_by_line_of_sight(self, x: int, y: int) -> int:
        # People don't just care about adjacent seats - they care about the
        # first seat they can see in each of those eight directions! Now,
        # instead of considering just the eight immediately adjacent seats,
        # consider the first seat in each of those eight directions.
        directions = [
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
        ]

        return sum(
            1
            for direction in directions
            if self.value_of_first_visible_seat_in_direction(x, y, direction)
            == GridValue.OCCUPIED_SEAT
        )

    def one_round_later(
        self,
        min_occupied_seats_for_occupied_seat_to_become_empty: int,
        neighbor_algorithm: WhichNeighborAlgorithmToUse,
    ) -> SeatGrid:
        # The following rules are applied to every seat simultaneously:
        new_seat_values = []

        for y in range(0, self.height):
            for x in range(0, self.width):
                value = self.value_at(x, y)

                neighbor_method = (
                    self.num_occupied_neighbors
                    if neighbor_algorithm
                    == WhichNeighborAlgorithmToUse.IMMEDIATELY_ADJACENT
                    else self.num_occupied_neighbors_by_line_of_sight
                )

                if value == GridValue.EMPTY_SEAT and neighbor_method(x, y) == 0:
                    # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
                    new_value = GridValue.OCCUPIED_SEAT
                elif (
                    value == GridValue.OCCUPIED_SEAT
                    and neighbor_method(x, y)
                    >= min_occupied_seats_for_occupied_seat_to_become_empty
                ):
                    # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
                    new_value = GridValue.EMPTY_SEAT
                else:
                    # Otherwise, the seat's state does not change.
                    new_value = value

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
        next_grid = grid.one_round_later(
            4, WhichNeighborAlgorithmToUse.IMMEDIATELY_ADJACENT
        )

        if grid == next_grid:
            break

        grid = next_grid

    return sum(1 for seat in grid.seats if seat == GridValue.OCCUPIED_SEAT)


def part_2() -> int:
    grid = load_input()

    # Given the new visibility method and the rule change for occupied seats
    # becoming empty, once equilibrium is reached, how many seats end up occupied?
    while True:
        next_grid = grid.one_round_later(5, WhichNeighborAlgorithmToUse.LINE_OF_SIGHT)

        if grid == next_grid:
            break

        grid = next_grid

    return sum(1 for seat in grid.seats if seat == GridValue.OCCUPIED_SEAT)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
