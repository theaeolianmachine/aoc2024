from enum import Enum


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


def turn_right(dir: Direction) -> Direction:
    if dir is Direction.NORTH:
        return Direction.EAST
    elif dir is Direction.EAST:
        return Direction.SOUTH
    elif dir is Direction.SOUTH:
        return Direction.WEST
    elif dir is Direction.WEST:
        return Direction.NORTH
    else:
        raise ValueError("Unknown Direction")


def parse_input() -> list[list[str]]:
    with open("day6/day6.txt") as fobj:
        return [list(line.strip()) for line in fobj.readlines()]


def find_bounds(maze: list[list[str]]) -> tuple[int, int]:
    return len(maze), len(maze[0])


def find_guard(maze: list[list[str]]) -> tuple[int, int]:
    for ri, row in enumerate(maze):
        if "^" in row:
            return ri, row.index("^")

    raise ValueError("Could not find guard, invalid maze.")


def in_bounds(maze: list[list[str]], ri: int, ci: int) -> bool:
    rlen, clen = find_bounds(maze)
    return ri >= 0 and ri < rlen and ci >= 0 and ci < clen


def find_next_loc(guard_row: int, guard_col: int, dir: Direction) -> tuple[int, int]:
    if dir is Direction.NORTH:
        return (guard_row - 1, guard_col)
    elif dir is Direction.EAST:
        return (guard_row, guard_col + 1)
    elif dir is Direction.SOUTH:
        return (guard_row + 1, guard_col)
    elif dir is Direction.WEST:
        return (guard_row, guard_col - 1)
    else:
        raise ValueError("Invalid Direction")


def get_guard_path(maze: list[list[str]]) -> set[tuple[int, int]]:
    guard_row, guard_col = find_guard(maze)
    distinct_pos: set[tuple[int, int]] = set(((guard_row, guard_col),))
    direction = Direction.NORTH

    next_ri, next_ci = find_next_loc(guard_row, guard_col, direction)
    while in_bounds(maze, next_ri, next_ci):
        while maze[next_ri][next_ci] == "#":
            direction = turn_right(direction)
            next_ri, next_ci = find_next_loc(guard_row, guard_col, direction)

        if not in_bounds(maze, next_ri, next_ci):
            break

        guard_row = next_ri
        guard_col = next_ci
        distinct_pos.add((guard_row, guard_col))

        next_ri, next_ci = find_next_loc(guard_row, guard_col, direction)

    return distinct_pos


def part_one(maze: list[list[str]]) -> int:
    distinct_pos = get_guard_path(maze)
    return len(distinct_pos)


def part_two(maze: list[list[str]]) -> int:
    num_loops = 0
    guard_row, guard_col = find_guard(maze)
    prev_turns: set[tuple[int, int, Direction]] = set()
    direction = Direction.NORTH
    guard_path = get_guard_path(maze)

    # Remove original starting position
    guard_path.remove((guard_row, guard_col))

    for obst_ri, obst_ci in guard_path:
        maze[obst_ri][obst_ci] = "#"
        in_loop = False

        next_ri, next_ci = find_next_loc(guard_row, guard_col, direction)
        while in_bounds(maze, next_ri, next_ci):
            while maze[next_ri][next_ci] == "#":
                if (guard_row, guard_col, direction) in prev_turns:
                    break
                prev_turns.add((guard_row, guard_col, direction))
                direction = turn_right(direction)
                next_ri, next_ci = find_next_loc(guard_row, guard_col, direction)

            if (guard_row, guard_col, direction) in prev_turns:
                in_loop = True
                break

            if not in_bounds(maze, next_ri, next_ci):
                in_loop = False
                break

            guard_row = next_ri
            guard_col = next_ci

            next_ri, next_ci = find_next_loc(guard_row, guard_col, direction)

        # Reset Maze State
        num_loops += 1 if in_loop else 0
        maze[obst_ri][obst_ci] = "."
        prev_turns.clear()
        guard_row, guard_col = find_guard(maze)
        direction = Direction.NORTH

    return num_loops


def main():
    maze = parse_input()
    print("Part One:")
    print(part_one(maze))
    print("Part Two:")
    print(part_two(maze))


if __name__ == "__main__":
    main()
