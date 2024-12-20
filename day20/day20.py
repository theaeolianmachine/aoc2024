from collections import deque


def parse_input() -> list[str]:
    with open("day20/day20.txt") as fobj:
        return [line.strip() for line in fobj.readlines()]


def valid_adjacent(ri: int, ci: int, racetrack: list[str]) -> bool:
    return (
        ri >= 0
        and ri < len(racetrack)
        and ci >= 0
        and ci < len(racetrack)
        and racetrack[ri][ci] != "#"
    )


def valid_adjacent_wall(ri: int, ci: int, racetrack: list[str]) -> bool:
    return (
        ri >= 0
        and ri < len(racetrack)
        and ci >= 0
        and ci < len(racetrack)
        and racetrack[ri][ci] == "#"
    )


def get_adjacent_nodes(ri: int, ci: int, racetrack: list[str]) -> set[tuple[int, int]]:
    all_adjacents: set[tuple[int, int]] = {
        (ri - 1, ci),
        (ri, ci + 1),
        (ri + 1, ci),
        (ri, ci - 1),
    }

    return {(ri, ci) for ri, ci in all_adjacents if valid_adjacent(ri, ci, racetrack)}


def get_adjacent_walls(ri: int, ci: int, racetrack: list[str]) -> set[tuple[int, int]]:
    all_adjacents: set[tuple[int, int]] = {
        (ri - 1, ci),
        (ri, ci + 1),
        (ri + 1, ci),
        (ri, ci - 1),
    }

    return {
        (ri, ci) for ri, ci in all_adjacents if valid_adjacent_wall(ri, ci, racetrack)
    }


def get_possible_cheat_nodes(
    ri: int, ci: int, racetrack: list[str]
) -> set[tuple[int, int]]:
    cheat_nodes: set[tuple[int, int]] = set()

    walls = get_adjacent_walls(ri, ci, racetrack)
    for wall in walls:
        valid_adjacents = {
            (ri, ci)
            for ri, ci in get_adjacent_nodes(wall[0], wall[1], racetrack)
            if valid_adjacent(ri, ci, racetrack)
        }
        cheat_nodes.update(valid_adjacents)

    return cheat_nodes


def part_one(racetrack: list[str]) -> int:
    num_cheats: int = 0

    start = (0, 0)
    end = (0, 0)

    # Find start and finish
    for ri, row in enumerate(racetrack):
        for ci, col in enumerate(row):
            if col == "S":
                start = (ri, ci)
            elif col == "E":
                end = (ri, ci)

    path = [start]
    explored = {start}
    to_explore = deque((start,))

    while to_explore:
        node = to_explore.popleft()
        if node == end:
            break
        for adj in get_adjacent_nodes(node[0], node[1], racetrack):
            if adj not in explored:
                explored.add(adj)
                # Only works because there is only one path
                path.append(adj)
                to_explore.append(adj)

    path_indexes: dict[tuple[int, int], int] = {}
    for i, loc in enumerate(path):
        path_indexes[loc] = i

    cheat_lengths: dict[int, int] = {}

    for ri, ci in path:
        possible_cheat_nodes = get_possible_cheat_nodes(ri, ci, racetrack)
        for cn in possible_cheat_nodes:
            if cn in path_indexes and path_indexes[cn] - 2 > path_indexes[(ri, ci)]:
                time_saved = path_indexes[cn] - 2 - path_indexes[(ri, ci)]
                cheat_lengths[time_saved] = cheat_lengths.setdefault(time_saved, 0) + 1

    # for cl in sorted(cheat_lengths):
    #     print(f"There are {cheat_lengths[cl]} cheats that save {cl} picoseconds")

    baseline_cheat = 100
    num_cheats = sum(
        [cheat_lengths[cl] for cl in cheat_lengths if cl >= baseline_cheat]
    )
    return num_cheats


def manhattan_distance(ri1: int, ci1: int, ri2: int, ci2: int) -> int:
    return abs(ri1 - ri2) + abs(ci1 - ci2)


def part_two(racetrack: list[str]):
    start = (0, 0)
    end = (0, 0)

    # Find start and finish
    for ri, row in enumerate(racetrack):
        for ci, col in enumerate(row):
            if col == "S":
                start = (ri, ci)
            elif col == "E":
                end = (ri, ci)

    path = [start]
    explored = {start}
    to_explore = deque((start,))

    while to_explore:
        node = to_explore.popleft()
        if node == end:
            break
        for adj in get_adjacent_nodes(node[0], node[1], racetrack):
            if adj not in explored:
                explored.add(adj)
                # Only works because there is only one path
                path.append(adj)
                to_explore.append(adj)

    path_indexes: dict[tuple[int, int], int] = {}
    for i, loc in enumerate(path):
        path_indexes[loc] = i

    cheat_lengths: dict[int, int] = {}

    for ri, ci in path:
        current_node_index = path_indexes[(ri, ci)]
        path_nodes_and_dist: dict[tuple[int, int], int] = {
            (ri2, ci2): manhattan_distance(ri, ci, ri2, ci2)
            for ri2, ci2 in path
            if manhattan_distance(ri, ci, ri2, ci2) <= 20
        }
        for node in path_nodes_and_dist:
            if path_indexes[node] - path_nodes_and_dist[node] > current_node_index:
                time_saved = (
                    path_indexes[node] - path_nodes_and_dist[node] - current_node_index
                )
                cheat_lengths[time_saved] = cheat_lengths.setdefault(time_saved, 0) + 1

    baseline_cheat = 100
    # for cl in sorted([cl for cl in cheat_lengths if cl >= baseline_cheat]):
    #     print(f"There are {cheat_lengths[cl]} cheats that save {cl} picoseconds")

    num_cheats = sum(
        [cheat_lengths[cl] for cl in cheat_lengths if cl >= baseline_cheat]
    )
    return num_cheats


def main():
    racetrack = parse_input()
    print("Part One:")
    print(part_one(racetrack))
    print("Part Two:")
    print(part_two(racetrack))


if __name__ == "__main__":
    main()
