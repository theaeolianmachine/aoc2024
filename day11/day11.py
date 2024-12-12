def parse_input() -> list[str]:
    with open("day11/day11.txt") as fobj:
        return [num for num in fobj.read().strip().split()]


def memoize(func):
    solutions = {}

    def memoized(*args):
        if args not in solutions:
            solutions[args] = func(*args)
        return solutions[args]

    return memoized


@memoize
def blink(stone: str, iterations: int) -> int:
    if iterations == 0:
        return 1
    elif stone == "0":
        return blink("1", iterations - 1)
    elif len(stone) % 2 == 0:
        mid = len(stone) // 2
        return blink(str(int(stone[:mid])), iterations - 1) + blink(
            str(int(stone[mid:])), iterations - 1
        )
    else:
        return blink(str(int(stone) * 2024), iterations - 1)


def part_one(stones: list[str]):
    num_stones = 0
    for stone in stones:
        num_stones += blink(stone, 25)

    return num_stones


def part_two(stones: list[str]):
    num_stones = 0
    for stone in stones:
        num_stones += blink(stone, 75)

    return num_stones


def main():
    stones = parse_input()
    print("Part One:")
    print(part_one(stones))
    print("Part Two:")
    print(part_two(stones))


if __name__ == "__main__":
    main()
