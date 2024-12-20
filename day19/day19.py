from functools import cache


def parse_input() -> tuple[list[str], list[str]]:
    with open("day19/day19.txt") as fobj:
        towels = fobj.readline().strip().split(", ")
        fobj.readline()
        designs = fobj.read().strip().split("\n")

    return towels, designs


def part_one(towels: list[str], designs: list[str]):
    solution_found = False

    def backtrack_design_solution(partial_solution: str, goal: str):
        nonlocal solution_found
        if solution_found:
            return

        if partial_solution == goal:
            solution_found = True
            return

        further_solutions = [f"{partial_solution}{towel}" for towel in towels]

        for candidate in further_solutions:
            if goal.startswith(candidate):
                backtrack_design_solution(candidate, goal)

    num_solutions = 0
    for design in designs:
        backtrack_design_solution("", design)
        if solution_found:
            num_solutions += 1
            solution_found = False

    return num_solutions


def part_two(towels: list[str], designs: list[str]):
    towels_set: set[str] = set(towels)
    min_towel_size: int = min(len(towel) for towel in towels_set)

    @cache
    def num_towel_solutions(goal: str) -> int:
        if len(goal) < min_towel_size:
            # No possible solution
            return 0
        elif len(goal) == min_towel_size and goal in towels_set:
            return 1
        num_solutions: int = 0
        for towel in towels_set:
            if goal == towel:
                num_solutions += 1
            if goal.endswith(towel):
                num_solutions += num_towel_solutions(goal[0 : len(goal) - len(towel)])

        return num_solutions

    num_solutions = 0
    for design in designs:
        num_solutions += num_towel_solutions(design)

    return num_solutions


def main():
    towels, designs = parse_input()
    print("Part One:")
    print(part_one(towels, designs))
    print("Part Two:")
    print(part_two(towels, designs))


if __name__ == "__main__":
    main()
