from dataclasses import dataclass


@dataclass
class Food:
    ingredients: list[str]
    allergens: list[str]


def load_input() -> list[Food]:
    with open("inputs/day_21.txt") as f:
        lines = [line.strip() for line in f]

    return [
        Food(
            line.split(" (contains ")[0].split(" "),
            line.split(" (contains ")[1][:-1].split(", "),
        )
        # line looks like "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)"
        for line in lines
    ]


# "Each allergen is found in exactly one ingredient. Each ingredient contains
# zero or one allergen. Allergens aren't always marked; when they're listed (as
# in (contains nuts, shellfish) after an ingredients list), the ingredient that
# contains each listed allergen will be somewhere in the corresponding
# ingredients list."
def allergen_candidates(foods: list[Food]) -> dict[str, set[str]]:
    allergens = set.union(*(set(food.allergens) for food in foods))

    return {
        allergen: set.intersection(
            *(set(food.ingredients) for food in foods if allergen in food.allergens)
        )
        for allergen in allergens
    }


def part_1() -> int:
    foods = load_input()
    candidates = allergen_candidates(foods)
    potentially_allergenic_ingredients = set.union(*candidates.values())

    # "Determine which ingredients cannot possibly contain any of the allergens
    # in your list. How many times do any of those ingredients appear?"
    return sum(
        1
        for food in foods
        for ingredient in food.ingredients
        if ingredient not in potentially_allergenic_ingredients
    )


def part_2() -> int:
    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
