from dataclasses import dataclass
from functools import cached_property, reduce


@dataclass
class Tile:
    id: int
    data: list[str]

    @cached_property
    def borders(self) -> tuple[str, str, str, str]:
        return (
            self.data[0],
            "".join(line[-1] for line in self.data),
            self.data[-1][::-1],
            "".join(line[0] for line in self.data)[::-1],
        )


@dataclass
class Match:
    tile_1_id: int
    tile_1_border_index: int
    tile_2_id: int
    tile_2_border_index: int
    when_tile_2_is_rotated_num_times: int


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

    return Tile(id=tile.id, data=rotated_data)


def load_input() -> list[Tile]:
    with open("inputs/day_20.txt") as f:
        lines = [line.strip() for line in f]

    result = []
    for i in range(0, len(lines), 12):
        tile_id = int(lines[i].split(" ")[1][:-1])
        tile_data = lines[i + 1 : i + 11]

        result.append(Tile(tile_id, tile_data))

    return result


def find_matches(tiles: list[Tile]) -> list[Match]:
    result = []
    for tile in tiles:
        other_tiles = [other_tile for other_tile in tiles if other_tile != tile]
        for other_tile in other_tiles:
            for num_times_tile_2_rotated in range(0, 4):
                for i, tile_border in enumerate(tile.borders):
                    tile_2_border_index_to_check = (i + 2) % 4
                    if (
                        tile_border
                        # TODO remove ::1s from this check and from .borders definition?
                        == other_tile.borders[tile_2_border_index_to_check]
                    ):
                        result.append(
                            Match(
                                tile.id,
                                i,
                                other_tile.id,
                                tile_2_border_index_to_check,
                                num_times_tile_2_rotated,
                            )
                        )

                other_tile = rotate_tile_right(other_tile)

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
        placed_tile_ids = {tile.id for tile in placed_tiles.values()}

        tile, relevant_matches = next(
            (tile, relevant_matches)
            for tile in unplaced_tiles
            if (
                relevant_matches := [
                    match
                    for match in matches
                    if match.tile_2_id == tile.id and match.tile_1_id in placed_tile_ids
                ]
            )
        )

        unplaced_tiles = [
            other_tile for other_tile in unplaced_tiles if other_tile != tile
        ]

        relevant_match = relevant_matches[0]

        for _ in range(relevant_match.when_tile_2_is_rotated_num_times):
            tile = rotate_tile_right(tile)

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

        assert position not in placed_tiles
        print(f"placing {tile.id=} at {position=}")
        placed_tiles[position] = tile

    return placed_tiles


def part_1() -> int:
    tiles = load_input()
    test_matching_handles_directionality_correctly()

    placed_tiles = place_tiles(tiles)

    print(placed_tiles)
    # return reduce(lambda x, y: x * y, [tile.id for tile in find_corners(tiles)])
    return -1


def part_2() -> int:
    return -1


def test_matching_handles_directionality_correctly() -> None:
    tile_1 = Tile(
        id=2957,
        data=[
            "###..#####",
            "###.......",
            "#..#.....#",
            "#.#......#",
            "#.....#..#",
            "#.#.......",
            "###.#..#.#",
            ".#.#.##.#.",
            "###.#.#...",
            "...##.####",
        ],
    )
    tile_2 = Tile(
        id=1093,
        data=[
            "#######.#.",
            "....#..#..",
            "...##.##..",
            "###.......",
            ".......#..",
            ".#...##..#",
            "......##.#",
            ".#....##..",
            "#.....#.##",
            "..#.#..###",
        ],
    )
    matches = find_matches([tile_1, tile_2])
    breakpoint()
    assert matches == []


def test_matching_can_find_next_tile_to_place() -> None:
    placed_tiles = [
        Tile(
            id=3079,
            data=[
                "#.#.#####.",
                ".#..######",
                "..#.......",
                "######....",
                "####.#..#.",
                ".#...#.##.",
                "#.#####.##",
                "..#.###...",
                "..#.......",
                "..#.###...",
            ],
        ),
        Tile(
            id=2311,
            data=[
                "..##.#..#.",
                "##..#.....",
                "#...##..#.",
                "####.#...#",
                "##.##.###.",
                "##...#.###",
                ".#.#.#..##",
                "..#....#..",
                "###...#.#.",
                "..###..###",
            ],
        ),
        Tile(
            id=2473,
            data=[
                "...###.#..",
                "#....##.##",
                "#..###.#..",
                "###..#.###",
                "##.######.",
                "...#.#.#.#",
                ".###.###.#",
                "..##.###.#",
                "...######.",
                "####...##.",
            ],
        ),
    ]

    tile_to_place = Tile(
        id=1171,
        data=[
            "####...##.",
            "#..##.#..#",
            "##.#..#.#.",
            ".###.####.",
            "..###.####",
            ".##....##.",
            ".#...####.",
            "#.##.####.",
            "####..#...",
            ".....##...",
        ],
    )


if __name__ == "__main__":
    print(part_1())
    print(part_2())
