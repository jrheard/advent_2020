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


def load_input() -> list[Tile]:
    with open("inputs/day_20.txt") as f:
        lines = [line.strip() for line in f]

    result = []
    for i in range(0, len(lines), 12):
        tile_id = int(lines[i].split(" ")[1][:-1])
        tile_data = lines[i + 1 : i + 11]

        borders = (
            tile_data[0],
            "".join(line[-1] for line in tile_data),
            tile_data[-1],
            "".join(line[0] for line in tile_data),
        )
        result.append(Tile(tile_id, borders, tile_data))

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
    placed_tiles = {(0, 0): first_corner}

    # The orientations of the .data and .borders of tiles in `unplaced_tiles` are arbitrary
    # with respect to all other tiles.
    unplaced_tiles = [tile for tile in tiles if tile != first_corner]

    while unplaced_tiles:
        matches = find_matches(list(placed_tiles.values()) + unplaced_tiles)

        for tile in unplaced_tiles:
            relevant_matches = [
                match
                for match in matches
                if match.tile_2_id == tile.id
                and match.tile_1_id in {tile.id for tile in placed_tiles.values()}
            ]
            if not relevant_matches:
                continue

            breakpoint()

            # TODO:
            # find (x, y) position of tile
            # correctly orient tile's borders
            # correctly orient tile's data
            # place that correctly oriented tile in placed_tiles

            # TODO will i need to recompute matches?
            # if not, how will i keep

            unplaced_tiles = [
                other_tile for other_tile in unplaced_tiles if other_tile != tile
            ]

    return placed_tiles


def part_1() -> int:
    tiles = load_input()
    place_tiles(tiles)
    # return reduce(lambda x, y: x * y, [tile.id for tile in find_corners(tiles)])
    return -1


def part_2() -> int:
    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
