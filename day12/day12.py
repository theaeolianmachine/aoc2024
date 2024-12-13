from collections import deque
from enum import Enum


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


def get_direction(ri: int, ci: int, ri2: int, ci2: int):
    if (ri - 1, ci) == (ri2, ci2):
        return Direction.NORTH
    elif (ri, ci + 1) == (ri2, ci2):
        return Direction.EAST
    elif (ri + 1, ci) == (ri2, ci2):
        return Direction.SOUTH
    elif (ri, ci - 1) == (ri2, ci2):
        return Direction.WEST
    else:
        raise ValueError("Not adjacent")


def parse_input() -> list[list[str]]:
    with open("day12/day12.txt") as fobj:
        return [[c for c in line.strip()] for line in fobj.readlines()]


def in_bounds(ri: int, ci: int, plots: list[list[str]]) -> bool:
    return ri >= 0 and ri < len(plots) and ci >= 0 and ci < len(plots[0])


def get_adj(ri: int, ci: int, plots: list[list[str]]) -> set[tuple[int, int]]:
    return {
        (r, c)
        for r, c in ((ri - 1, ci), (ri, ci + 1), (ri + 1, ci), (ri, ci - 1))
        if in_bounds(r, c, plots)
    }


def get_neighbor_plants(
    ri: int, ci: int, plant_type: str, plots: list[list[str]]
) -> set[tuple[int, int]]:
    adj_plants = get_adj(ri, ci, plots)
    return {(nri, nci) for nri, nci in adj_plants if plots[nri][nci] == plant_type}


def find_region(
    start_ri: int, start_ci: int, plant_type: str, plots: list[list[str]]
) -> dict[tuple[int, int], int]:
    visited: dict[tuple[int, int], int] = {}
    encountered_queue: deque[tuple[int, int]] = deque()

    perimeter = 4 - len(
        get_neighbor_plants(start_ri, start_ci, plots[start_ri][start_ci], plots)
    )
    visited[(start_ri, start_ci)] = perimeter
    encountered_queue.append((start_ri, start_ci))

    while encountered_queue:
        ri, ci = encountered_queue.popleft()
        neighbor_plants = get_neighbor_plants(ri, ci, plant_type, plots)
        visited[(ri, ci)] = 4 - len(neighbor_plants)
        for nri, nci in neighbor_plants:
            if (nri, nci) not in visited:
                visited[(nri, nci)] = -1
                encountered_queue.append((nri, nci))

    return visited


def count_sides(
    plant_type: str, region: set[tuple[int, int]], plots: list[list[str]]
) -> int:
    total_sides = 0
    side_segments: set[tuple[tuple[int, int], Direction]] = set()
    for ri, ci in sorted(region):
        possible_sides = {
            ((r, c), get_direction(ri, ci, r, c))
            for r, c in ((ri - 1, ci), (ri, ci + 1), (ri + 1, ci), (ri, ci - 1))
            if not in_bounds(r, c, plots) or plots[r][c] != plant_type
        }
        for loc, dir in possible_sides:
            if dir in (Direction.NORTH, Direction.SOUTH):
                possible_adj = ((loc[0], loc[1] - 1), (loc[0], loc[1] + 1))
            else:
                possible_adj = ((loc[0] - 1, loc[1]), (loc[0] + 1, loc[1]))
            if not any((adj_loc, dir) in side_segments for adj_loc in possible_adj):
                total_sides += 1
            side_segments.add((loc, dir))

    return total_sides


def part_one(plots: list[list[str]]) -> int:
    regions: dict[str, list[dict[tuple[int, int], int]]] = {}
    visited_plants: set[tuple[int, int]] = set()
    for ri in range(len(plots)):
        for ci in range(len(plots[ri])):
            if (ri, ci) in visited_plants:
                continue
            else:
                cur_region = find_region(ri, ci, plots[ri][ci], plots)
                cur_plant_regions = regions.setdefault(plots[ri][ci], [])
                cur_plant_regions.append(cur_region)
                visited_plants.update(cur_region)

    total_cost = 0
    for plant_type in regions:
        for region in regions[plant_type]:
            area = len(region.keys())
            perimeter = sum(region.values())
            total_cost += area * perimeter

    return total_cost


def part_two(plots: list[list[str]]):
    regions: dict[str, list[dict[tuple[int, int], int]]] = {}
    visited_plants: set[tuple[int, int]] = set()
    for ri in range(len(plots)):
        for ci in range(len(plots[ri])):
            if (ri, ci) in visited_plants:
                continue
            else:
                cur_region = find_region(ri, ci, plots[ri][ci], plots)
                cur_plant_regions = regions.setdefault(plots[ri][ci], [])
                cur_plant_regions.append(cur_region)
                visited_plants.update(cur_region)

    total_cost = 0
    for plant_type in regions:
        for region in regions[plant_type]:
            area = len(region.keys())
            num_sides = count_sides(plant_type, set(region.keys()), plots)
            total_cost += area * num_sides

    return total_cost


def main():
    garden_plots = parse_input()
    print("Part One:")
    print(part_one(garden_plots))
    print("Part Two:")
    print(part_two(garden_plots))


if __name__ == "__main__":
    main()
