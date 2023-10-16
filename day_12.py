from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"


DIRECTIONS_IN_ORDER = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

DELTAS_BY_DIRECTION = {
    Direction.NORTH: [0, -1],
    Direction.EAST: [1, 0],
    Direction.SOUTH: [0, 1],
    Direction.WEST: [-1, 0],
}


@dataclass(frozen=True)
class Ship:
    facing_direction: Direction
    position: tuple[int, int]

    # TODO annotate as union of str literals l and r?
    def turn_in_relative_direction(self, relative_direction: str, value: int) -> Ship:
        current_direction_index = DIRECTIONS_IN_ORDER.index(self.facing_direction)

        value_in_indexes = value / 90

        multiplier = -1 if relative_direction == "L" else 1

        new_index = current_direction_index + int(value_in_indexes * multiplier)

        # We don't want to use modulus here because it doesn't handle negative numbers the way we want (eg -1 % 4 == 3, not -1)
        if new_index >= 4:
            new_index -= 4

        return Ship(
            facing_direction=DIRECTIONS_IN_ORDER[new_index],
            position=self.position,
        )

    def move_in_direction(self, direction: Direction, value: int) -> Ship:
        x_delta, y_delta = DELTAS_BY_DIRECTION[direction]
        return Ship(
            facing_direction=self.facing_direction,
            position=(
                self.position[0] + x_delta * value,
                self.position[1] + y_delta * value,
            ),
        )

    def process_action(self, action: tuple[str, int]) -> Ship:
        match action:
            case "L" | "R", action_value:
                return self.turn_in_relative_direction(*action)
            case "F", action_value:
                return self.move_in_direction(self.facing_direction, action_value)
            case direction_str, action_value:
                return self.move_in_direction(Direction(direction_str), action_value)
            case _:
                raise ValueError(f"Invalid action {action}")


def load_input() -> list[tuple[str, int]]:
    with open("inputs/day_12.txt") as f:
        return [(line[0], int(line[1:].strip())) for line in f]


def part_1() -> int:
    # "The ship starts by facing east."
    ship = Ship(Direction.EAST, (0, 0))

    for action in load_input():
        ship = ship.process_action(action)

    # Figure out where the navigation instructions lead. What is the Manhattan
    # distance between that location and the ship's starting position?
    return abs(ship.position[0]) + abs(ship.position[1])


def part_2() -> int:
    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
