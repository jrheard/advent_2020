from typing import Iterator


def load_input() -> tuple[int, list[int]]:
    # Your notes (your puzzle input) consist of two lines. The first line is
    # your estimate of the earliest timestamp you could depart on a bus. The
    # second line lists the bus IDs that are in service according to the shuttle
    # company; entries that show x must be out of service, so you decide to
    # ignore them.
    with open("inputs/day_13.txt") as f:
        lines = [line.strip() for line in f]

    departure_timestamp = int(lines[0])
    available_bus_ids = [int(bus_id) for bus_id in lines[1].split(",") if bus_id != "x"]

    return departure_timestamp, available_bus_ids


def part_1() -> int:
    departure_timestamp, bus_ids = load_input()

    departed_minutes_ago_per_bus = [departure_timestamp % bus_id for bus_id in bus_ids]

    # Bus schedules are defined based on a timestamp that measures the number of
    # minutes since some fixed reference point in the past. At timestamp 0,
    # every bus simultaneously departed from the sea port. After that, each bus
    # travels to the airport, then various other locations, and finally returns
    # to the sea port to repeat its journey forever.
    # The time this loop takes a particular bus is also its ID number: the bus
    # with ID 5 departs from the sea port at timestamps 0, 5, 10, 15, and so on.
    # The bus with ID 11 departs at 0, 11, 22, 33, and so on. If you are there
    # when the bus departs, you can ride that bus to the airport!
    minutes_until_departure_per_bus = [
        bus_ids[i] - departed_minutes_ago
        for i, departed_minutes_ago in enumerate(departed_minutes_ago_per_bus)
    ]

    soonest_bus_index = min(
        enumerate(minutes_until_departure_per_bus),
        key=lambda index_and_minutes: index_and_minutes[1],
    )[0]

    # What is the ID of the earliest bus you can take to the airport multiplied
    # by the number of minutes you'll need to wait for that bus?
    return (
        bus_ids[soonest_bus_index] * minutes_until_departure_per_bus[soonest_bus_index]
    )


def load_indexes_and_bus_ids() -> list[tuple[int, int]]:
    with open("inputs/day_13.txt") as f:
        lines = [line.strip() for line in f]

    return [
        (i, int(bus_id))
        for i, bus_id in enumerate(lines[1].split(","))
        if bus_id != "x"
    ]


def generate_potential_timestamps_for_contest(
    largest_bus_index: int, largest_bus_id: int
) -> Iterator[int]:
    i = 1
    while True:
        yield largest_bus_id * i - largest_bus_index
        i += 1


def part_2() -> int:
    indexes_and_bus_ids = sorted(
        load_indexes_and_bus_ids(),
        key=lambda index_and_id: index_and_id[1],
        reverse=True,
    )
    largest_bus_index, largest_bus_id = max(
        indexes_and_bus_ids, key=lambda index_and_id: index_and_id[1]
    )

    last_printed_timestamp = 0
    for timestamp in generate_potential_timestamps_for_contest(
        largest_bus_index, largest_bus_id
    ):
        if timestamp > last_printed_timestamp * 10:
            print(timestamp)
            last_printed_timestamp = timestamp
        if all(
            timestamp % bus_id == bus_id - index
            for index, bus_id in indexes_and_bus_ids
        ):
            return timestamp

    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
