from collections import defaultdict


STARTING_NUMBERS = [13, 0, 10, 12, 1, 5, 8]


def run_game_through_turn(end_turn: int) -> int:
    turn = 1
    turns_on_which_number_was_spoken = defaultdict(list)
    most_recent_number = 0

    while turn <= end_turn:
        if turn <= len(STARTING_NUMBERS):
            most_recent_number = number_to_speak = STARTING_NUMBERS[turn - 1]
        else:
            turns = turns_on_which_number_was_spoken[most_recent_number]
            if len(turns) == 1:
                # If that was the first time the number has been spoken, the current
                # player says 0.
                number_to_speak = 0
            else:
                # Otherwise, the number had been spoken before; the
                # current player announces how many turns apart the number is from
                # when it was previously spoken.
                number_to_speak = turns[-1] - turns[-2]

        turns_on_which_number_was_spoken[number_to_speak].append(turn)
        most_recent_number = number_to_speak
        turn += 1

    return most_recent_number


def part_1() -> int:
    return run_game_through_turn(2020)


def part_2() -> int:
    return run_game_through_turn(30000000)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
