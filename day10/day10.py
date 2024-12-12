from collections import deque


def parse_input() -> list[list[int]]:
    with open("day10/day10.txt") as fobj:
        return [[int(c) for c in line.strip()] for line in fobj.readlines()]


def part_one(topo_map: list[list[int]]) -> int:
    reachable_summits = 0
    trail_heads = {
        (ri, ci)
        for ri in range(len(topo_map))
        for ci in range(len(topo_map[ri]))
        if topo_map[ri][ci] == 0
    }

    for th in trail_heads:
        reachable_summits += find_paths_to_top(topo_map, th)

    return reachable_summits


def part_two(topo_map: list[list[int]]) -> int:
    reachable_summits = 0
    trail_heads = {
        (ri, ci)
        for ri in range(len(topo_map))
        for ci in range(len(topo_map[ri]))
        if topo_map[ri][ci] == 0
    }

    for th in trail_heads:
        reachable_summits += find_all_paths_to_top(topo_map, th)

    return reachable_summits


def in_bounds(ri: int, ci: int, topo_map: list[list[int]]) -> bool:
    return ri >= 0 and ri < len(topo_map) and ci >= 0 and ci < len(topo_map[0])


def get_adjacent_pos(
    ri: int, ci: int, topo_map: list[list[int]]
) -> set[tuple[int, int]]:
    adjacents = {(ri - 1, ci), (ri, ci + 1), (ri + 1, ci), (ri, ci - 1)}

    return {loc for loc in adjacents if in_bounds(loc[0], loc[1], topo_map)}


def find_paths_to_top(topo_map: list[list[int]], trail_head: tuple[int, int]) -> int:
    num_paths = 0
    visited: set[tuple[int, int]] = set()
    encountered_queue: deque[tuple[int, int]] = deque()
    encountered_queue.append(trail_head)

    while encountered_queue:
        ri, ci = encountered_queue.popleft()
        height = topo_map[ri][ci]
        if height == 9:
            num_paths += 1
            continue
        adj_pos = get_adjacent_pos(ri, ci, topo_map)
        valid_pos = {
            (ari, aci) for ari, aci in adj_pos if topo_map[ari][aci] == height + 1
        }

        for ri, ci in valid_pos:
            if (ri, ci) not in visited:
                visited.add((ri, ci))
                encountered_queue.append((ri, ci))

    return num_paths


def find_all_paths_to_top(
    topo_map: list[list[int]], trail_head: tuple[int, int]
) -> int:
    num_paths = 0
    encountered_queue: deque[tuple[int, int]] = deque()
    encountered_queue.append(trail_head)

    while encountered_queue:
        ri, ci = encountered_queue.popleft()
        height = topo_map[ri][ci]
        if height == 9:
            num_paths += 1
            continue
        adj_pos = get_adjacent_pos(ri, ci, topo_map)
        valid_pos = {
            (ari, aci) for ari, aci in adj_pos if topo_map[ari][aci] == height + 1
        }

        for ri, ci in valid_pos:
            encountered_queue.append((ri, ci))

    return num_paths


def main():
    topo_map = parse_input()
    print("Part One:")
    print(part_one(topo_map))
    print("Part Two:")
    print(part_two(topo_map))


if __name__ == "__main__":
    main()
