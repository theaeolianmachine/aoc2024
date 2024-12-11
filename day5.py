from functools import cmp_to_key


def parse_input() -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    with open("day5.txt") as fobj:
        lines = fobj.readlines()

    split_index = lines.index("\n")

    rules = [line.strip() for line in lines[:split_index]]
    rules = [tuple(int(page) for page in line.split("|")) for line in rules]
    updates = [line.strip() for line in lines[split_index + 1 :]]
    updates = [tuple(int(page) for page in line.split(",")) for line in updates]

    return rules, updates


def part_one(rules: list[tuple[int, ...]], updates: list[tuple[int, ...]]) -> int:
    rules_set: dict[int, set[int]] = {}
    middle_sums = 0
    for key, value in rules:
        vset = rules_set.setdefault(key, set())
        vset.add(value)

    for update in updates:
        is_valid = True

        for i, page in enumerate(update):
            remainder = update[i + 1 :]
            is_valid = all(
                num not in rules_set or page not in rules_set[num] for num in remainder
            )
            if not is_valid:
                break

        if is_valid:
            middle_sums += update[len(update) // 2]

    return middle_sums


def part_two(rules: list[tuple[int, ...]], updates: list[tuple[int, ...]]) -> int:
    rules_set: dict[int, set[int]] = {}
    middle_sums = 0
    for key, value in rules:
        vset = rules_set.setdefault(key, set())
        vset.add(value)

    def cmp_func(x, y):
        if x in rules_set and y in rules_set[x]:
            return -1
        if y in rules_set and x in rules_set[y]:
            return 1
        return 0

    for update in updates:
        sorted_update = list(sorted(update, key=cmp_to_key(cmp_func)))
        if list(update) != sorted_update:
            middle_sums += sorted_update[len(sorted_update) // 2]

    return middle_sums


def main():
    rules, updates = parse_input()
    print("Part One:")
    print(part_one(rules, updates))
    print("Part Two:")
    print(part_two(rules, updates))


if __name__ == "__main__":
    main()
