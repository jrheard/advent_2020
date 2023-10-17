import functools

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
    field_ranges, _, nearby_tickets = parse_input()

    return sum(
        find_invalid_value_in_ticket(ticket, field_ranges) for ticket in nearby_tickets
    )


def part_2() -> int:
    field_ranges, your_ticket, nearby_tickets = parse_input()

    valid_tickets = [
        ticket
        for ticket in nearby_tickets
        if find_invalid_value_in_ticket(ticket, field_ranges) == 0
    ]

    # `your_ticket` has N ordered field values - right now, any one of those values
    # could correspond to any field (eg 'departure location', 'arrival platform', etc).
    field_candidates_by_index = [
        set(field_ranges.keys()) for _ in range(len(valid_tickets[0]))
    ]

    # First, we eliminate all of the fields that _definitely_ can't possibly live at a particular index
    # by seeing which indexes have invalid values for each field.
    # For instance, if we have this rule:
    #   departure location: 32-174 or 190-967
    # and if a ticket has the value 180 at index 0,
    # then we know that index 0 can't be for the field "departure location".
    for ticket in valid_tickets:
        for i, field_value in enumerate(ticket):
            for candidate_field in field_candidates_by_index[i].copy():
                range_1, range_2 = field_ranges[candidate_field]
                if not (
                    range_1[0] <= field_value <= range_1[1]
                    or range_2[0] <= field_value <= range_2[1]
                ):
                    field_candidates_by_index[i].remove(candidate_field)

    # At this point, the way that our inputs are structured, we'll be left with one index
    # that has a clear answer (i.e. has exactly one candidate field), and another index with
    # two possible fields, and another index with three fields, etc.
    #
    # All we need to do now is use process of elimination - e.g. if the field 'row' has been proven
    # to live at index 2, it definitely cannot live at any other index.

    field_indexes_by_field_name = {}

    while any(len(candidates) > 0 for candidates in field_candidates_by_index):
        index, converged_field = next(
            (i, candidates.pop())
            for i, candidates in enumerate(field_candidates_by_index)
            if len(candidates) == 1
        )
        field_indexes_by_field_name[converged_field] = index

        for candidates in field_candidates_by_index:
            if len(candidates) > 0:
                candidates.remove(converged_field)

    # Done!
    assert len(field_indexes_by_field_name) == len(your_ticket)

    # "Once you work out which field is which, look for the six fields on your
    # ticket that start with the word departure. What do you get if you multiply
    # those six values together?"
    return functools.reduce(
        lambda x, y: x * y,
        (
            your_ticket[index]
            for field_name, index in field_indexes_by_field_name.items()
            if field_name.startswith("departure")
        ),
    )


if __name__ == "__main__":
    print(part_1())
    print(part_2())
