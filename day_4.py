import re

from util import load_line_groups_from_file


def height_is_valid(passport_value: str) -> bool:
    if passport_value.endswith("cm"):
        return 150 <= int(passport_value[:-2]) <= 193
    elif passport_value.endswith("in"):
        return 59 <= int(passport_value[:-2]) <= 76
    else:
        return False


PASSPORT_FIELD_VALIDATORS = {
    "byr": lambda v: 1920 <= int(v) <= 2002,
    "iyr": lambda v: 2010 <= int(v) <= 2020,
    "eyr": lambda v: 2020 <= int(v) <= 2030,
    "hgt": height_is_valid,
    "hcl": lambda v: re.match(r"#[0-9a-f]{6,6}", v),
    "ecl": lambda v: v in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
    "pid": lambda v: re.match(r"^\d{9,9}$", v),
    "cid": lambda v: True,
}


ALL_PASSPORT_FIELDS = PASSPORT_FIELD_VALIDATORS.keys()


def parse_input() -> list[dict[str, str]]:
    # input file has groups of lines like

    # iyr:1928 cid:150 pid:476113241 eyr:2039 hcl:a5ac0f
    # ecl:#25f8d2
    # byr:2027 hgt:190
    #
    # hgt:168cm eyr:2026 ecl:hzl hcl:#fffffd cid:169 pid:920076943
    # byr:1929 iyr:2013
    grouped_lines = load_line_groups_from_file("inputs/day_4.txt")

    passports = []

    for group in grouped_lines:
        passport_in_progress = {}
        for line in group:
            for item in line.split(" "):
                key, value = item.split(":")
                passport_in_progress[key] = value

        passports.append(passport_in_progress)

    return passports


def does_passport_have_required_keys(passport: dict[str, str]) -> bool:
    # it's ok to be missing 'cid', but all other fields must be present
    missing_keys = ALL_PASSPORT_FIELDS - set(passport.keys())
    return not missing_keys or missing_keys == {"cid"}


def is_passport_valid(passport: dict[str, str]) -> bool:
    return does_passport_have_required_keys(passport) and all(
        PASSPORT_FIELD_VALIDATORS[k](v) for (k, v) in passport.items()
    )


def part_1() -> int:
    passports = parse_input()
    return sum(
        1 for passport in passports if does_passport_have_required_keys(passport)
    )


def part_2() -> int:
    passports = parse_input()
    return sum(1 for passport in passports if is_passport_valid(passport))


if __name__ == "__main__":
    print(part_1())
    print(part_2())
