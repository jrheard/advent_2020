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
    bag_rules = parse_input()

    colors_to_look_for = {"shiny gold"}
    colors_known_to_contain_shiny_gold = set()
    colors_to_check = set(bag_rules.keys()) - {"shiny gold"}

    while colors_to_look_for:
        # Pop off a color to look for, like "shiny gold".
        color_to_look_for = colors_to_look_for.pop()

        bags_that_contain_the_color = set(
            color_to_check
            for color_to_check in colors_to_check
            if any(
                bag_name == color_to_look_for
                for _, bag_name in bag_rules[color_to_check]
            )
        )

        # At this point we've found all of the colors of bags that directly contain that color.
        # This means that those colors of bags can all eventually contain shiny gold bags!
        colors_known_to_contain_shiny_gold |= bags_that_contain_the_color
        colors_to_look_for |= bags_that_contain_the_color
        colors_to_check -= bags_that_contain_the_color

    return len(colors_known_to_contain_shiny_gold)


def part_2() -> int:
    # How many individual bags are required inside your single shiny gold bag?
    bag_rules = parse_input()

    # "So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags
    # within it) plus 2 vibrant plum bags (and the 11 bags within **each** of
    # those): 1 + 1*7 + 2 + 2*11 = 32 bags!"
    #
    # The "each" there is important, so our `colors_to_check` worklist tracks tuples of (multiplier, color).
    colors_to_check = {(1, "shiny gold")}
    num_bags_required = 0

    while colors_to_check:
        multiplier, color_to_check = colors_to_check.pop()

        num_bags_required += sum(
            num * multiplier for num, _ in bag_rules[color_to_check]
        )
        colors_to_check |= set(
            (multiplier * num, color) for num, color in bag_rules[color_to_check]
        )

    return num_bags_required


if __name__ == "__main__":
    print(part_1())
    print(part_2())
