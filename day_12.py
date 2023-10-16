from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal


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


def compute_new_direction_relative_to_old_one(
    old_direction: Direction, relative_direction: Literal["L", "R"], degrees: int
) -> Direction:
    current_direction_index = DIRECTIONS_IN_ORDER.index(old_direction)

    value_in_indexes = degrees / 90

    multiplier = -1 if relative_direction == "L" else 1

    new_index = current_direction_index + int(value_in_indexes * multiplier)

    # We don't want to use modulus here because it doesn't handle negative numbers the way we want (eg -1 % 4 == 3, not -1)
    if new_index >= 4:
        new_index -= 4

    return DIRECTIONS_IN_ORDER[new_index]


@dataclass(frozen=True)
class Ship:
    facing_direction: Direction
    position: tuple[int, int]

    def turn_in_relative_direction(
        self, relative_direction: Literal["L", "R"], degrees: int
    ) -> Ship:
        return Ship(
            facing_direction=compute_new_direction_relative_to_old_one(
                self.facing_direction, relative_direction, degrees
            ),
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


def rotate_waypoint_right(waypoint_x: int, waypoint_y: int) -> tuple[int, int]:
    return (-waypoint_y, waypoint_x)


def rotate_waypoint_left(waypoint_x: int, waypoint_y: int) -> tuple[int, int]:
    return (waypoint_y, -waypoint_x)


@dataclass(frozen=True)
class WaypointedShip:
    position: tuple[int, int]
    waypoint: tuple[int, int]

    def move_waypoint_in_direction(
        self, direction: Direction, value: int
    ) -> WaypointedShip:
        x_delta, y_delta = DELTAS_BY_DIRECTION[direction]
        return WaypointedShip(
            position=self.position,
            waypoint=(
                self.waypoint[0] + x_delta * value,
                self.waypoint[1] + y_delta * value,
            ),
        )

    def move_waypoint_in_relative_direction(
        self, relative_direction: Literal["L", "R"], degrees: int
    ) -> WaypointedShip:
        move_fn = (
            rotate_waypoint_left if relative_direction == "L" else rotate_waypoint_right
        )
        num_times = degrees // 90
        new_waypoint = self.waypoint
        for _ in range(num_times):
            new_waypoint = move_fn(*new_waypoint)

        return WaypointedShip(position=self.position, waypoint=new_waypoint)

    def move_to_waypoint(self, num_times: int) -> WaypointedShip:
        new_x, new_y = self.position
        for _ in range(num_times):
            new_x += self.waypoint[0]
            new_y += self.waypoint[1]

        return WaypointedShip(position=(new_x, new_y), waypoint=self.waypoint)

    def process_action(self, action: tuple[str, int]) -> WaypointedShip:
        match action:
            case "L" | "R", action_value:
                return self.move_waypoint_in_relative_direction(*action)
            case "F", action_value:
                return self.move_to_waypoint(action_value)
            case direction_str, action_value:
                return self.move_waypoint_in_direction(
                    Direction(direction_str), action_value
                )
            case _:
                raise ValueError(f"Invalid action {action}")


def part_2() -> int:
    # The waypoint starts 10 units east and 1 unit north relative to the ship.
    ship = WaypointedShip((0, 0), (10, -1))

    for action in load_input():
        ship = ship.process_action(action)

    # Figure out where the navigation instructions lead. What is the Manhattan
    # distance between that location and the ship's starting position?
    return abs(ship.position[0]) + abs(ship.position[1])


if __name__ == "__main__":
    print(part_1())
    print(part_2())
