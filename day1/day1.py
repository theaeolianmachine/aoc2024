from collections import Counter


def parse_lists() -> tuple[list[int], list[int]]:
    list_one: list[int] = []
    list_two: list[int] = []

    with open("day1/day1.txt") as fobj:
        input_lines = fobj.readlines()
    for line in input_lines:
        first, second = line.strip().split()
        list_one.append(int(first))
        list_two.append(int(second))

    return list_one, list_two


def part_one(list_one: list[int], list_two: list[int]) -> int:
    distances: list[int] = []
    index = 0

    assert len(list_one) == len(list_two)

    while index < len(list_one) and index < len(list_two):
        dist_one = list_one[index]
        dist_two = list_two[index]
        distances.append(abs(dist_two - dist_one))
        index += 1

    return sum(distances)


def part_two(list_one: list[int], list_two: list[int]) -> int:
    similarities: list[int] = []
    list_two_counter = Counter(list_two)

    for dist in list_one:
        if dist in list_two_counter:
            similarity = dist * list_two_counter[dist]
        else:
            similarity = 0
        similarities.append(similarity)

    return sum(similarities)


def main():
    list_one, list_two = parse_lists()
    list_one.sort()
    list_two.sort()

    print("Part One:")
    print(part_one(list_one, list_two))

    print("Part Two:")
    print(part_two(list_one, list_two))


if __name__ == "__main__":
    main()
