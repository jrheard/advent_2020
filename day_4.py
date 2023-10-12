ALL_PASSPORT_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}


def parse_input() -> list[dict[str:str]]:
    # input file has groups of lines like

    # iyr:1928 cid:150 pid:476113241 eyr:2039 hcl:a5ac0f
    # ecl:#25f8d2
    # byr:2027 hgt:190
    #
    # hgt:168cm eyr:2026 ecl:hzl hcl:#fffffd cid:169 pid:920076943
    # byr:1929 iyr:2013

    with open("inputs/day_4.txt") as f:
        lines = [line.strip() for line in f]

    passports = []
    passport_in_progress = {}

    for line in lines:
        if line == "":
            passports.append(passport_in_progress)
            passport_in_progress = {}

        else:
            for item in line.split(" "):
                key, value = item.split(":")
                passport_in_progress[key] = value

    return passports


def is_passport_valid(passport: dict[str, str]) -> bool:
    # it's ok to be missing 'cid', but all other fields must be present
    missing_keys = ALL_PASSPORT_FIELDS - set(passport.keys())
    return not missing_keys or missing_keys == {"cid"}


def part_1() -> int:
    passports = parse_input()
    return sum(1 for passport in passports if is_passport_valid(passport))


def part_2() -> int:
    pass


if __name__ == "__main__":
    print(part_1())
    print(part_2())
