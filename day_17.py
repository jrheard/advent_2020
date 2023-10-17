# 3d game of life on an infinite board, interesting.
# Can't use a 1d list this time, oh well.

from dataclasses import dataclass


@dataclass
class Bounds:
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int


Coordinates = tuple[int, int, int]


def load_input() -> tuple[set[Coordinates], Bounds]:
    with open("inputs/day_17.txt") as f:
        lines = [line.strip() for line in f]

    active_cells = set()

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                active_cells.add((x, y, 0))

    return active_cells, Bounds(0, len(lines[0]) - 1, 0, len(lines) - 1, 0, 0)


def find_neighbor_coordinates(x, y, z) -> list[tuple[int, int, int]]:
    return [
        (xx, yy, zz)
        for xx in range(x - 1, x + 2)
        for yy in range(y - 1, y + 2)
        for zz in range(z - 1, z + 2)
        if (xx, yy, zz) != (x, y, z)
    ]


def advance_one_step(
    active_coordinates: set[Coordinates], bounds: Bounds
) -> tuple[set[Coordinates], Bounds]:
    active_coordinates = active_coordinates.copy()

    for x in range(bounds.min_x - 1, bounds.max_x + 1):
        for y in range(bounds.min_y - 1, bounds.max_y + 1):
            for z in range(bounds.min_z - 1, bounds.max_z + 1):
                num_active_neighbors = sum(
                    1
                    for coords in find_neighbor_coordinates(x, y, z)
                    if coords in active_coordinates
                )

                coords = (x, y, z)

                if coords in active_coordinates:
                    # If a cube is active and exactly 2 or 3 of its neighbors are
                    # also active, the cube remains active. Otherwise, the cube becomes inactive.
                    if num_active_neighbors not in (2, 3):
                        active_coordinates.remove(coords)

                else:
                    # If a cube is inactive but exactly 3 of its neighbors are
                    # active, the cube becomes active. Otherwise, the cube remains inactive.
                    if num_active_neighbors == 3:
                        active_coordinates.add(coords)

    return active_coordinates, Bounds(
        bounds.min_x - 1,
        bounds.max_x + 1,
        bounds.min_y - 1,
        bounds.max_y + 1,
        bounds.min_z - 1,
        bounds.max_z + 1,
    )


def part_1() -> int:
    active_coordinates, bounds = load_input()
    for _ in range(6):
        active_coordinates, bounds = advance_one_step(active_coordinates, bounds)

    return len(active_coordinates)


def part_2() -> int:
    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
