def load_map() -> list[str]:
    with open("inputs/day_3.txt") as f:
        return [line.strip() for line in f]


def part_1() -> int:
    tree_map = load_map()
    map_width = len(tree_map[0])

    x, y = 0, 0
    num_trees_seen = 0

    while y < len(tree_map):
        if tree_map[y][x] == "#":
            num_trees_seen += 1

        x = (x + 3) % map_width
        y += 1

    return num_trees_seen


def part_2() -> int:
    pass


if __name__ == "__main__":
    print(part_1())
    print(part_2())
