from collections import deque
from enum import Enum, auto


class WhichPlayer(Enum):
    ME = auto()
    CRAB = auto()


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


# Returns the player that wins, as well as their score.
def recursive_combat(
    player_deck: deque[int],
    crab_deck: deque[int],
) -> tuple[WhichPlayer, int]:
    player_deck_configurations = set()
    crab_deck_configurations = set()

    while True:
        # "Before either player deals a card, if there was a previous round in this
        # game that had exactly the same cards in the same order in the same
        # players' decks, the game instantly ends in a win for player 1. Previous
        # rounds from other games are not considered. (This prevents infinite games
        # of Recursive Combat, which everyone agrees is a bad idea.)"
        if (
            tuple(player_deck) in player_deck_configurations
            and tuple(crab_deck) in crab_deck_configurations
        ):
            return WhichPlayer.ME, score_deck(player_deck)

        player_deck_configurations.add(tuple(player_deck))
        crab_deck_configurations.add(tuple(crab_deck))

        player_card = player_deck.popleft()
        crab_card = crab_deck.popleft()

        if len(player_deck) >= player_card and len(crab_deck) >= crab_card:
            # "If both players have at least as many cards remaining in their deck as the
            # value of the card they just drew, the winner of the round is determined by
            # playing a new game of Recursive Combat."
            #
            # "Each player creates a new deck by making a copy of the next cards in
            # their deck (the quantity of cards copied is equal to the number on the
            # card they drew to trigger the sub-game). During this sub-game, the
            # game that triggered it is on hold and completely unaffected; no cards
            # are removed from players' decks to form the sub-game."
            winner, _ = recursive_combat(
                deque(list(player_deck)[:player_card]),
                deque(list(crab_deck)[:crab_card]),
            )

        elif player_card > crab_card:
            # "Otherwise, at least one player must not have enough cards left in
            # their deck to recurse; the winner of the round is the player with the
            # higher-value card."
            winner = WhichPlayer.ME
        else:
            winner = WhichPlayer.CRAB

        # "As in regular Combat, the winner of the round (even if they won the
        # round by winning a sub-game) takes the two cards dealt at the
        # beginning of the round and places them on the bottom of their own deck
        # (again so that the winner's card is above the other card)."
        if winner == WhichPlayer.ME:
            player_deck.append(player_card)
            player_deck.append(crab_card)
        else:
            crab_deck.append(crab_card)
            crab_deck.append(player_card)

        # "If collecting cards by winning the round causes a player to have all
        # of the cards, they win, and the game ends."
        if not player_deck:
            return WhichPlayer.CRAB, score_deck(crab_deck)
        elif not crab_deck:
            return WhichPlayer.ME, score_deck(player_deck)


def part_2() -> int:
    player_deck, crab_deck = load_input()

    return recursive_combat(player_deck, crab_deck)[1]


if __name__ == "__main__":
    print(part_1())
    print(part_2())
