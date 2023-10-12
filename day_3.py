def load_map() -> list[str]:
    with open("inputs/day_3.txt") as f:
        return [line.strip() for line in f]


def find_num_trees_on_slope(tree_map: list[str], slope: tuple[int, int]) -> int:
    tree_map = load_map()
    map_width = len(tree_map[0])

    # You start on the open square (.) in the top-left corner and need to reach
    # the bottom (below the bottom-most row on your map).
    x, y = 0, 0
    num_trees_seen = 0

    while y < len(tree_map):
        if tree_map[y][x] == "#":
            num_trees_seen += 1

        y += slope[1]
        # Due to something you read about once involving arboreal genetics and
        # biome stability, the same pattern repeats to the right many times.
        x = (x + slope[0]) % map_width

    return num_trees_seen


def part_1() -> int:
    # The toboggan can only follow a few specific slopes (you opted for a
    # cheaper model that prefers rational numbers); start by counting all the
    # trees you would encounter for the slope right 3, down 1.
    return find_num_trees_on_slope(load_map(), (3, 1))


def part_2() -> int:
    tree_map = load_map()
    result = 1

    # Determine the number of trees you would encounter if, for each of the
    # following slopes, you start at the top-left corner and traverse the map
    # all the way to the bottom.
    for slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        result *= find_num_trees_on_slope(tree_map, slope)

    return result


if __name__ == "__main__":
    print(part_1())
    print(part_2())
