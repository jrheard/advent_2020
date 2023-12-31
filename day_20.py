from dataclasses import dataclass
from functools import cached_property, reduce
from typing import Collection, Iterator, Sequence


@dataclass
class Tile:
    id: int
    data: list[str]

    @cached_property
    def borders(self) -> tuple[str, str, str, str]:
        return (
            self.data[0],
            "".join(line[-1] for line in self.data),
            self.data[-1],
            "".join(line[0] for line in self.data),
        )


@dataclass
class Match:
    tile_1_id: int
    tile_1_border_index: int
    tile_2_id: int
    tile_2_border_index: int
    when_tile_2_is_rotated_num_times: int
    when_tile_2_is_flipped: bool


def print_tile_data(tile: Tile) -> None:
    print(f"Tile {tile.id}:")
    print()
    for line in tile.data:
        print(line)


def rotate_image_right(image: list[str]) -> list[str]:
    rotated_image = ["" for _ in image]

    for line in image:
        for i, char in enumerate(line):
            rotated_image[i] = char + rotated_image[i]

    return rotated_image


def flip_image(image: list[str]) -> list[str]:
    return [line[::-1] for line in image]


def rotate_tile_right(tile: Tile) -> Tile:
    return Tile(id=tile.id, data=rotate_image_right(tile.data))


def flip_tile(tile: Tile) -> Tile:
    return Tile(id=tile.id, data=flip_image(tile.data))


def load_input() -> list[Tile]:
    with open("inputs/day_20.txt") as f:
        lines = [line.strip() for line in f]

    result = []
    for i in range(0, len(lines), 12):
        tile_id = int(lines[i].split(" ")[1][:-1])
        tile_data = lines[i + 1 : i + 11]

        result.append(Tile(tile_id, tile_data))

    return result


def try_to_match_tiles(tile_1: Tile, tile_2: Tile) -> Match | None:
    for tile_2_was_flipped in (False, True):
        for num_times_tile_2_rotated in range(4):
            for i, tile_border in enumerate(tile_1.borders):
                tile_2_border_index_to_check = (i + 2) % 4
                if tile_border == tile_2.borders[tile_2_border_index_to_check]:
                    return Match(
                        tile_1.id,
                        i,
                        tile_2.id,
                        tile_2_border_index_to_check,
                        num_times_tile_2_rotated,
                        tile_2_was_flipped,
                    )

            tile_2 = rotate_tile_right(tile_2)

        tile_2 = flip_tile(tile_2)


def find_first_match(
    placed_tiles: Collection[Tile], unplaced_tiles: Sequence[Tile]
) -> Match | None:
    for tile in placed_tiles:
        for other_tile in unplaced_tiles:
            if (match := try_to_match_tiles(tile, other_tile)) is not None:
                return match


def place_tiles(tiles: list[Tile]) -> dict[tuple[int, int], Tile]:
    first_tile = tiles[0]

    # The orientations of the .data and .borders of tiles in `placed_tiles` are authoritative.
    placed_tiles: dict[tuple[int, int], Tile] = {(0, 0): first_tile}

    # The orientations of the .data and .borders of tiles in `unplaced_tiles` are arbitrary
    # with respect to all other tiles.
    unplaced_tiles = tiles[1:]

    while unplaced_tiles:
        # print(len(placed_tiles), len(unplaced_tiles))

        match = find_first_match(placed_tiles.values(), unplaced_tiles)
        assert match is not None
        tile = next(tile for tile in unplaced_tiles if match.tile_2_id == tile.id)

        unplaced_tiles = [
            other_tile for other_tile in unplaced_tiles if other_tile != tile
        ]

        # Orient `tile` to the correct position as per the instructions in `match`.
        # Note that it's important to first flip and _then_ rotate,
        # because that's the order that `try_to_match_tiles()` does it in.
        if match.when_tile_2_is_flipped:
            tile = flip_tile(tile)

        for _ in range(match.when_tile_2_is_rotated_num_times):
            tile = rotate_tile_right(tile)

        # Now all we have to do is figure out this tile's placement position.
        placed_tile_x, placed_tile_y = next(
            position
            for position, placed_tile in placed_tiles.items()
            if placed_tile.id == match.tile_1_id
        )

        if match.tile_1_border_index == 0:
            position = (placed_tile_x, placed_tile_y - 1)
        elif match.tile_1_border_index == 1:
            position = (placed_tile_x + 1, placed_tile_y)
        elif match.tile_1_border_index == 2:
            position = (placed_tile_x, placed_tile_y + 1)
        else:
            position = (placed_tile_x - 1, placed_tile_y)

        assert position not in placed_tiles
        # print(f"placing {tile.id=} at {position=}")
        placed_tiles[position] = tile

    return placed_tiles


def get_bounds(placed_tiles: dict[tuple[int, int], Tile]) -> tuple[int, int, int, int]:
    return (
        min(x for (x, _) in placed_tiles.keys()),
        max(x for (x, _) in placed_tiles.keys()),
        min(y for (_, y) in placed_tiles.keys()),
        max(y for (_, y) in placed_tiles.keys()),
    )


def part_1() -> int:
    tiles = load_input()

    placed_tiles = place_tiles(tiles)
    min_x, max_x, min_y, max_y = get_bounds(placed_tiles)

    return (
        placed_tiles[(min_x, min_y)].id
        * placed_tiles[(min_x, max_y)].id
        * placed_tiles[(max_x, max_y)].id
        * placed_tiles[(max_x, min_y)].id
    )


# Now, you're ready to search for sea monsters! Because your image is monochrome, a sea monster will look like this:
#
#                   #
#   #    ##    ##    ###
#  #  #  #  #  #  #
SEA_MONSTER_COORDINATES = [
    (18, 0),
    (0, 1),
    (5, 1),
    (6, 1),
    (11, 1),
    (12, 1),
    (17, 1),
    (18, 1),
    (19, 1),
    (1, 2),
    (4, 2),
    (7, 2),
    (10, 2),
    (13, 2),
    (16, 2),
]


def count_sea_monsters_in_image(image: list[str]) -> int:
    result = 0
    for y in range(len(image) - 2):
        for x in range(len(image[0]) - 20):
            if all(
                image[y + yy][x + xx] == "#" for (xx, yy) in SEA_MONSTER_COORDINATES
            ):
                result += 1

    return result


def part_2() -> int:
    tiles = load_input()

    placed_tiles = place_tiles(tiles)
    min_x, max_x, min_y, max_y = get_bounds(placed_tiles)

    # "The borders of each tile are not part of the actual image; start by removing them."
    image = []
    for y in range(min_y, max_y + 1):
        for yy in range(1, 9):
            line = ""
            for x in range(min_x, max_x + 1):
                tile = placed_tiles[(x, y)]
                line += tile.data[yy][1:9]

            image.append(line)

    num_monster_hashes = 0

    for _ in range(4):
        image = rotate_image_right(image)
        if (num_monsters := count_sea_monsters_in_image(image)) > 0:
            num_monster_hashes = num_monsters * len(SEA_MONSTER_COORDINATES)

    image = flip_image(image)

    for _ in range(4):
        image = rotate_image_right(image)
        if (num_monsters := count_sea_monsters_in_image(image)) > 0:
            num_monster_hashes = num_monsters * len(SEA_MONSTER_COORDINATES)

    # Determine how rough the waters are in the sea monsters' habitat by
    # counting the number of # that are not part of a sea monster. In the above
    # example, the habitat's water roughness is 273.
    # How many # are not part of a sea monster?
    num_hashes = sum(1 for char in "".join(image) if char == "#")

    return num_hashes - num_monster_hashes


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
    match = find_first_match([tile_1], [tile_2])
    assert match == Match(
        tile_1_id=2957,
        tile_1_border_index=3,
        tile_2_id=1093,
        tile_2_border_index=1,
        when_tile_2_is_rotated_num_times=1,
        when_tile_2_is_flipped=False,
    )


def test_matching() -> None:
    tile_1 = Tile(
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
    )
    tile_2 = Tile(
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
    )
    match = find_first_match([tile_1], [tile_2])
    assert match == Match(
        tile_1_id=2311,
        tile_1_border_index=1,
        tile_2_id=3079,
        tile_2_border_index=3,
        when_tile_2_is_rotated_num_times=2,
        when_tile_2_is_flipped=True,
    )


def test_counting() -> None:
    image = """.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###""".split(
        "\n"
    )
    assert count_sea_monsters_in_image(image) == 0

    image = rotate_image_right(image)
    assert count_sea_monsters_in_image(image) == 0
    image = rotate_image_right(image)
    assert count_sea_monsters_in_image(image) == 0
    image = rotate_image_right(image)
    assert count_sea_monsters_in_image(image) == 0

    image = flip_image(image)
    assert count_sea_monsters_in_image(image) == 0
    image = rotate_image_right(image)
    assert count_sea_monsters_in_image(image) == 0
    image = rotate_image_right(image)
    assert count_sea_monsters_in_image(image) == 2
    image = rotate_image_right(image)
    assert count_sea_monsters_in_image(image) == 0


if __name__ == "__main__":
    test_counting()
    test_matching()
    test_matching_handles_directionality_correctly()
    print(part_1())
    print(part_2())
