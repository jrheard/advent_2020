from dataclasses import dataclass


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


def part_1() -> int:
    tiles = load_input()
    matches = find_matches(tiles)
    from pprint import pprint

    pprint(matches)
    return -1


def part_2() -> int:
    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
