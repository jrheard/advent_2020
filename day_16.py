# The type of a dict representing input lines like:
#     departure location: 32-174 or 190-967
# with data like this:
#     'departure location': ((32, 174), (190, 967))
FieldRanges = dict[str, tuple[tuple[int, int], tuple[int, int]]]


def parse_input() -> tuple[FieldRanges, tuple[int], tuple[tuple[int]]]:
    with open("inputs/day_16.txt") as f:
        lines = [line.strip() for line in f]

    field_ranges = {}

    for line in lines[:20]:
        # a line like "departure location: 32-174 or 190-967"
        field = line[: line.find(":")]

        # ["32-174", "190-967"]
        range_strings = line.split(": ")[1].split(" or ")

        ranges = []
        for range_string in range_strings:
            int_strings = range_string.split("-")
            ranges.append((int(int_strings[0]), int(int_strings[1])))

        field_ranges[field] = tuple(ranges)

    your_ticket = tuple(map(int, lines[22].split(",")))

    nearby_tickets = tuple(tuple(map(int, line.split(","))) for line in lines[25:])

    return (field_ranges, your_ticket, nearby_tickets)


def find_invalid_value_in_ticket(ticket: tuple[int], field_ranges: FieldRanges) -> int:
    for field_value in ticket:
        value_is_valid_for_any_field = False
        for range_1, range_2 in field_ranges.values():
            if (
                range_1[0] <= field_value <= range_1[1]
                or range_2[0] <= field_value <= range_2[1]
            ):
                value_is_valid_for_any_field = True

        if not value_is_valid_for_any_field:
            return field_value

    return 0


def part_1() -> int:
    field_ranges, your_ticket, nearby_tickets = parse_input()

    return sum(
        find_invalid_value_in_ticket(ticket, field_ranges) for ticket in nearby_tickets
    )


def part_2() -> int:
    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
