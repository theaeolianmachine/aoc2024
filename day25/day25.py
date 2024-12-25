import itertools


def parse_input() -> tuple[list[list[int]], list[list[int]]]:
    with open("day25/day25.txt") as fobj:
        lines = fobj.readlines()

    keys: list[list[int]] = []
    locks: list[list[int]] = []

    new_key: list[int] = []
    new_lock: list[int] = []
    for line in lines:
        if line == "\n":
            if new_key:
                keys.append(new_key)
                new_key = []
            elif new_lock:
                locks.append(new_lock)
                new_lock = []
        elif line.startswith(".....") and not new_lock and not new_key:
            new_key = [5] * 5
        elif line.startswith("#####") and not new_key and not new_lock:
            new_lock = [0] * 5
        elif new_key:
            for i, char in enumerate(line.strip()):
                if char == ".":
                    new_key[i] -= 1
        elif new_lock:
            for i, char in enumerate(line.strip()):
                if char == "#":
                    new_lock[i] += 1
    if new_key:
        keys.append(new_key)
    elif new_lock:
        locks.append(new_lock)

    return keys, locks


def part_one(keys: list[list[int]], locks: list[list[int]]):
    num_matches: int = 0
    for key, lock in itertools.product(keys, locks):
        match_found = True
        for i in range(len(key)):
            if key[i] + lock[i] >= 6:
                match_found = False
                break
        if match_found:
            num_matches += 1
    return num_matches


def part_two():
    return "Hooray, you delivered the Chronicle to Santa!"


def main():
    keys, locks = parse_input()
    print("Part One:")
    print(part_one(keys, locks))
    print("Part Two:")
    print(part_two())


if __name__ == "__main__":
    main()
