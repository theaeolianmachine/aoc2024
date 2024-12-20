from collections import deque


def parse_input():
    with open("day18/day18.txt") as fobj:
        lines = fobj.read().strip().split("\n")
    corrupted: list[tuple[int, int]] = []
    for line in lines:
        split_line = line.split(",")
        corrupted.append((int(split_line[0]), int(split_line[1])))
    return corrupted


def is_valid_move(
    x: int, y: int, xend: int, yend: int, corrupted: set[tuple[int, int]]
) -> bool:
    return x >= 0 and x <= xend and y >= 0 and y <= yend and (x, y) not in corrupted


def get_valid_moves(
    x: int, y: int, xend: int, yend: int, corrupted: set[tuple[int, int]]
) -> set[tuple[int, int]]:
    return {
        (mx, my)
        for mx, my in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y))
        if is_valid_move(mx, my, xend, yend, corrupted)
    }


def part_one(corrupted: list[tuple[int, int]]):
    first_kilo_corrupted = corrupted[:1024]
    corrupted_set = set(first_kilo_corrupted)
    start = (0, 0)
    goal = (70, 70)

    explored: set[tuple[int, int]] = {(start[0], start[1])}
    to_explore: deque[tuple[int, int, int]] = deque(((start[0], start[1], 0),))

    while to_explore:
        x, y, dist = to_explore.popleft()
        if (x, y) == goal:
            return dist
        valid_moves = get_valid_moves(x, y, 70, 70, corrupted_set)
        for move in valid_moves:
            if move not in explored:
                explored.add(move)
                to_explore.append((move[0], move[1], dist + 1))


def part_two(corrupted: list[tuple[int, int]]):
    start = (0, 0)
    goal = (70, 70)

    # Lol. Could have binary searched? Oh well, I'll take it after Day 17.
    for i in range(1, len(corrupted)):
        partial_corrupted = corrupted[0:i]
        corrupted_set = set(partial_corrupted)

        found_goal = False
        explored: set[tuple[int, int]] = {(start[0], start[1])}
        to_explore: deque[tuple[int, int, int]] = deque(((start[0], start[1], 0),))
        while to_explore:
            x, y, dist = to_explore.popleft()
            if (x, y) == goal:
                found_goal = True
                break
            valid_moves = get_valid_moves(x, y, 70, 70, corrupted_set)
            for move in valid_moves:
                if move not in explored:
                    explored.add(move)
                    to_explore.append((move[0], move[1], dist + 1))

        if not found_goal:
            x, y = partial_corrupted[-1]
            return f"{x},{y}"


def main():
    corrupted = parse_input()
    print("Part One:")
    print(part_one(corrupted))
    print("Part Two:")
    print(part_two(corrupted))


if __name__ == "__main__":
    main()
