from dataclasses import dataclass
from functools import reduce


@dataclass
class Tile:
    id: int
    # Borders are stored in the order (top, right, bottom, left).
    borders: tuple[str, str, str, str]
    data: list[str]


@dataclass
class Match:
    tile_1_id: int
    tile_1_border_index: int
    tile_2_id: int
    tile_2_border_index: int


def print_tile_data(tile: Tile) -> None:
    print(f"Tile {tile.id}:")
    print()
    for line in tile.data:
        print(line)


def rotate_tile_right(tile: Tile) -> Tile:
    # print(f"rotating {tile.id} to the right")
    rotated_data = ["" for _ in tile.data]

    for line in tile.data:
        for i, char in enumerate(line):
            rotated_data[i] = char + rotated_data[i]

    return Tile(id=tile.id, borders=borders_from_data(rotated_data), data=rotated_data)


def borders_from_data(data: list[str]) -> tuple[str, str, str, str]:
    return (
        data[0],
        "".join(line[-1] for line in data),
        data[-1],
        "".join(line[0] for line in data),
    )


def load_input() -> list[Tile]:
    with open("inputs/day_20.txt") as f:
        lines = [line.strip() for line in f]

    result = []
    for i in range(0, len(lines), 12):
        tile_id = int(lines[i].split(" ")[1][:-1])
        tile_data = lines[i + 1 : i + 11]

        result.append(Tile(tile_id, borders_from_data(tile_data), tile_data))

    return result


def find_matches(tiles: list[Tile]) -> list[Match]:
    result = []
    for tile in tiles:
        other_tiles = [other_tile for other_tile in tiles if other_tile != tile]
        for other_tile in other_tiles:
            for i, tile_border in enumerate(tile.borders):
                for j, other_tile_border in enumerate(other_tile.borders):
                    if (
                        tile_border == other_tile_border
                        or tile_border == other_tile_border[::-1]
                    ):
                        result.append(Match(tile.id, i, other_tile.id, j))

    return result


def place_tiles(tiles: list[Tile]) -> dict[tuple[int, int], Tile]:
    matches = find_matches(tiles)

    first_corner = next(
        tile
        for tile in tiles
        if len([match for match in matches if match.tile_1_id == tile.id]) == 2
    )

    # The orientations of the .data and .borders of tiles in `placed_tiles` are authoritative.
    placed_tiles: dict[tuple[int, int], Tile] = {(0, 0): first_corner}

    # The orientations of the .data and .borders of tiles in `unplaced_tiles` are arbitrary
    # with respect to all other tiles.
    unplaced_tiles = [tile for tile in tiles if tile != first_corner]

    while unplaced_tiles:
        print(len(placed_tiles), len(unplaced_tiles))
        matches = find_matches(list(placed_tiles.values()) + unplaced_tiles)

        tile, relevant_matches = next(
            (tile, relevant_matches)
            for tile in unplaced_tiles
            if (
                relevant_matches := [
                    match
                    for match in matches
                    if match.tile_2_id == tile.id
                    and match.tile_1_id in {tile.id for tile in placed_tiles.values()}
                ]
            )
        )

        unplaced_tiles = [
            other_tile for other_tile in unplaced_tiles if other_tile != tile
        ]

        relevant_match = relevant_matches[0]

        # Remember, a match looks like this:
        #   Match(tile_1_id=1117, tile_1_border_index=3, tile_2_id=2003, tile_2_border_index=2)

        # relevant_match.tile_1_id is a placed tile whose position and orientation are fully known.
        # relevant_match.tile_2_id is `tile`, whose position is unknown and whose orientation is arbitrary.

        # First, let's figure out `tile`'s correct orientation.
        # If the match occurs along tile 1's east border, then it occurs along tile 2's west border;
        # if it occurs along tile 1's south border, then it occurs along tile 2's north border; etc.

        correctly_rotated_tile_2_border_index = (
            relevant_match.tile_1_border_index + 2
        ) % 4

        # If correctly_rotated_tile_2_border_index == relevant_match.tile_2_border_index, then we're all set.
        # Otherwise, we need to rotate tile 2 to the right 1-3 times.
        num_times_rotated_right = 0
        while (
            relevant_match.tile_2_border_index + num_times_rotated_right
        ) % 4 != correctly_rotated_tile_2_border_index:
            tile = rotate_tile_right(tile)
            num_times_rotated_right += 1

        # Now all we have to do is figure out this tile's placement position.
        placed_tile_x, placed_tile_y = next(
            position
            for position, placed_tile in placed_tiles.items()
            if placed_tile.id == relevant_match.tile_1_id
        )
        if relevant_match.tile_1_border_index == 0:
            position = (placed_tile_x, placed_tile_y - 1)
        elif relevant_match.tile_1_border_index == 1:
            position = (placed_tile_x + 1, placed_tile_y)
        elif relevant_match.tile_1_border_index == 2:
            position = (placed_tile_x, placed_tile_y + 1)
        else:
            position = (placed_tile_x - 1, placed_tile_y)

        if position in placed_tiles:
            breakpoint()

        assert position not in placed_tiles
        placed_tiles[position] = tile

    return placed_tiles


def part_1() -> int:
    tiles = load_input()
    placed_tiles = place_tiles(tiles)
    print(placed_tiles)
    # return reduce(lambda x, y: x * y, [tile.id for tile in find_corners(tiles)])
    return -1


def part_2() -> int:
    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
