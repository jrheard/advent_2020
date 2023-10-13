from util import load_line_groups_from_file


def parse_input() -> dict[str, list[tuple[int, str]]]:
    """Returns a dict of {color: color_contents} like:
    {
        'plaid fuchsia': [(3, 'shiny yellow'), (2, 'shiny maroon'), (1, 'clear aqua')],
        'dim purple': [(4, 'light crimson'), (2, 'dotted yellow'), (2,'mirrored maroon')],
        'dark salmon': [(2, 'faded teal'), (4, 'drab white'), (3, 'posh bronze')],
        'drab maroon': [],
    }
    """
    with open("inputs/day_7.txt") as f:
        lines = [line.strip() for line in f]

    # lines look like either of these:
    # dark salmon bags contain 2 faded teal bags, 4 drab white bags, 3 posh bronze bags.
    # drab maroon bags contain no other bags.
    result = {}
    for line in lines:
        second_space_idx = line.find(" ", line.find(" ") + 1)
        color = line[:second_space_idx]

        if line.endswith("no other bags."):
            second_space_idx = line.find(" ", line.find(" ") + 1)
            result[color] = []
        else:
            contents = line[line.find("contain") + 8 : -1]
            result[color] = [
                (
                    int(number_and_color_string[0]),
                    number_and_color_string[2 : number_and_color_string.find(" bag")],
                )
                for number_and_color_string in contents.split(", ")
            ]

    return result


def part_1() -> int:
    # You have a shiny gold bag. If you wanted to carry it in at least one other
    # bag, how many different bag colors would be valid for the outermost bag?
    # (In other words: how many colors can, eventually, contain at least one shiny gold bag?)
    print(parse_input())
    return 1


def part_2() -> int:
    return 1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
