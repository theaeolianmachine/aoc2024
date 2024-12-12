from itertools import combinations


def parse_input() -> list[list[str]]:
    with open("day8.txt") as fobj:
        return [list(line.strip()) for line in fobj.readlines()]


def in_bounds(ri: int, ci: int, map: list[list[str]]) -> bool:
    return ri >= 0 and ri < len(map) and ci >= 0 and ci < len(map[0])


def get_resonant_antinodes(
    ant_one: tuple[int, int], ant_two: tuple[int, int], map: list[list[str]]
) -> list[tuple[int, int]]:
    # Include Antennas
    antinodes = [ant_one, ant_two]
    r_dist = ant_two[0] - ant_one[0]
    c_dist = ant_two[1] - ant_one[1]

    # Backwards Search
    cand_r = ant_one[0] - r_dist
    cand_c = ant_one[1] - c_dist

    while in_bounds(cand_r, cand_c, map):
        antinodes.append((cand_r, cand_c))
        cand_r -= r_dist
        cand_c -= c_dist

    # Forwards Search
    cand_r = ant_two[0] + r_dist
    cand_c = ant_two[1] + c_dist

    while in_bounds(cand_r, cand_c, map):
        antinodes.append((cand_r, cand_c))
        cand_r += r_dist
        cand_c += c_dist

    return antinodes


def get_antinodes(
    ant_one: tuple[int, int], ant_two: tuple[int, int], map: list[list[str]]
) -> list[tuple[int, int]]:
    r_dist = ant_two[0] - ant_one[0]
    c_dist = ant_two[1] - ant_one[1]
    antinodes = []

    if in_bounds(ant_one[0] - r_dist, ant_one[1] - c_dist, map):
        antinodes.append((ant_one[0] - r_dist, ant_one[1] - c_dist))

    if in_bounds(ant_two[0] + r_dist, ant_two[1] + c_dist, map):
        antinodes.append((ant_two[0] + r_dist, ant_two[1] + c_dist))

    return antinodes

    # 3, 4 and 5, 5 == 1, 3 and 7, 6
    # Dist is 2, 1

    # X - Dist: Good
    # X + Dist: Equals Y
    # Y + Dist: Good
    # Y - Dist: Equals X

    # 4, 8 and 5, 5 == 3, 11 and 6, 2
    # Dist is 1, -3
    # X - Dist: Good
    # X + Dist: Equals Y
    # Y + Dist: Good
    # Y - Dist: Equals X


def part_one(antenna_map: list[list[str]]):
    antennas: dict[str, list[tuple[int, int]]] = {}
    for ri, row in enumerate(antenna_map):
        for ci, col in enumerate(row):
            if col.isalnum():
                locs = antennas.setdefault(col, [])
                locs.append((ri, ci))

    antinodes: set[tuple[int, int]] = set()
    for antenna in antennas:
        for ant_one, ant_two in combinations(antennas[antenna], 2):
            antinodes.update(get_antinodes(ant_one, ant_two, antenna_map))

    return len(antinodes)


def part_two(antenna_map: list[list[str]]):
    antennas: dict[str, list[tuple[int, int]]] = {}
    for ri, row in enumerate(antenna_map):
        for ci, col in enumerate(row):
            if col.isalnum():
                locs = antennas.setdefault(col, [])
                locs.append((ri, ci))

    antinodes: set[tuple[int, int]] = set()
    for antenna in antennas:
        for ant_one, ant_two in combinations(antennas[antenna], 2):
            antinodes.update(get_resonant_antinodes(ant_one, ant_two, antenna_map))

    return len(antinodes)


def main():
    antenna_map = parse_input()
    print("Part One:")
    print(part_one(antenna_map))
    print("Part Two:")
    print(part_two(antenna_map))


if __name__ == "__main__":
    main()
