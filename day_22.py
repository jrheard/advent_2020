from collections import deque


def load_input() -> tuple[deque[int], deque[int]]:
    with open("inputs/day_22.txt") as f:
        lines = [line.strip() for line in f]

    midpoint = lines.index("")

    return (
        deque(int(card) for card in lines[1:midpoint]),
        deque(int(card) for card in lines[midpoint + 2 :]),
    )


# "The bottom card in their deck is worth the value of the card multiplied by 1,
# the second-from-the-bottom card is worth the value of the card multiplied by
# 2, and so on. With 10 cards, the top card is worth the value on the card
# multiplied by 10."
def score_deck(deck: deque[int]) -> int:
    return sum(card * (i + 1) for i, card in enumerate(reversed(deck)))


def part_1() -> int:
    player_deck, crab_deck = load_input()

    while player_deck and crab_deck:
        player_card = player_deck.popleft()
        crab_card = crab_deck.popleft()

        if player_card > crab_card:
            player_deck.append(player_card)
            player_deck.append(crab_card)
        else:
            crab_deck.append(crab_card)
            crab_deck.append(player_card)

    winning_deck = next(deck for deck in (player_deck, crab_deck) if deck)
    return score_deck(winning_deck)


def part_2() -> int:
    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
