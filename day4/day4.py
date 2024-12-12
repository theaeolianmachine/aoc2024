def in_bounds(x: int, y: int, width: int, height: int) -> bool:
    return x > -1 and x < width and y > -1 and y < height


def parse_input() -> list[str]:
    with open("day4/day4.txt") as fobj:
        return [line.strip() for line in fobj.readlines()]


def part_one(word_search: list[str]):
    width = len(word_search[0])
    height = len(word_search)

    matches = 0

    for ri, row in enumerate(word_search):
        for ci, col in enumerate(row):
            if col == "X":
                # Found a potential match
                matches += find_matches(word_search, ri, ci, width, height)

    return matches


def part_two(word_search: list[str]):
    width = len(word_search[0])
    height = len(word_search)

    matches = 0

    for ri, row in enumerate(word_search):
        for ci, col in enumerate(row):
            if col == "A":
                matches += 1 if is_x_match(word_search, ri, ci, width, height) else 0

    return matches


def is_x_match(
    word_search: list[str], ri: int, ci: int, width: int, height: int
) -> bool:
    coordinates = [
        (ri - 1, ci - 1),
        (ri + 1, ci - 1),
        (ri - 1, ci + 1),
        (ri + 1, ci + 1),
    ]
    all_in_bounds = all([in_bounds(y, x, width, height) for y, x in coordinates])
    if not all_in_bounds:
        return False

    def mas_match(r1: int, c1: int, r2: int, c2: int) -> bool:
        return (word_search[r1][c1] == "S" and word_search[r2][c2] == "M") or (
            word_search[r1][c1] == "M" and word_search[r2][c2] == "S"
        )

    return mas_match(ri - 1, ci - 1, ri + 1, ci + 1) and mas_match(
        ri + 1, ci - 1, ri - 1, ci + 1
    )


def find_matches(
    word_search: list[str], ri: int, ci: int, width: int, height: int
) -> int:
    search = "XMAS"
    num_matches = 0

    # Horizontal
    is_match = True
    for i in range(1, len(search)):
        if (
            not in_bounds(ci + i, ri, width, height)
            or search[i] != word_search[ri][ci + i]
        ):
            is_match = False
            break

    num_matches += 1 if is_match else 0

    is_match = True
    for i in range(1, len(search)):
        if (
            not in_bounds(ci - i, ri, width, height)
            or search[i] != word_search[ri][ci - i]
        ):
            is_match = False
            break

    num_matches += 1 if is_match else 0

    # Vertical
    is_match = True
    for i in range(1, len(search)):
        if (
            not in_bounds(ci, ri + i, width, height)
            or search[i] != word_search[ri + i][ci]
        ):
            is_match = False
            break

    num_matches += 1 if is_match else 0

    is_match = True
    for i in range(1, len(search)):
        if (
            not in_bounds(ci, ri - i, width, height)
            or search[i] != word_search[ri - i][ci]
        ):
            is_match = False
            break

    num_matches += 1 if is_match else 0

    # Diagonal Left
    is_match = True
    for i in range(1, len(search)):
        if (
            not in_bounds(ci - i, ri - i, width, height)
            or search[i] != word_search[ri - i][ci - i]
        ):
            is_match = False
            break

    num_matches += 1 if is_match else 0

    is_match = True
    for i in range(1, len(search)):
        if (
            not in_bounds(ci - i, ri + i, width, height)
            or search[i] != word_search[ri + i][ci - i]
        ):
            is_match = False
            break

    num_matches += 1 if is_match else 0

    # Diagonal Right
    is_match = True
    for i in range(1, len(search)):
        if (
            not in_bounds(ci + i, ri - i, width, height)
            or search[i] != word_search[ri - i][ci + i]
        ):
            is_match = False
            break

    num_matches += 1 if is_match else 0

    is_match = True
    for i in range(1, len(search)):
        if (
            not in_bounds(ci + i, ri + i, width, height)
            or search[i] != word_search[ri + i][ci + i]
        ):
            is_match = False
            break

    num_matches += 1 if is_match else 0

    return num_matches


def main():
    word_search = parse_input()
    print("Part One:")
    print(part_one(word_search))
    print("Part Two:")
    print(part_two(word_search))


if __name__ == "__main__":
    main()
