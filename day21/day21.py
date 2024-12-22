from collections.abc import Sequence
from functools import cache
from itertools import permutations, product


def parse_input() -> list[str]:
    with open("day21/day21.txt") as fobj:
        return fobj.read().strip().split("\n")


def generate_keypads() -> tuple[dict[str, tuple[int, int]], dict[str, tuple[int, int]]]:
    numeric_keypad_strs: list[str] = ["789", "456", "123", "G0A"]
    numeric_keypad: dict[str, tuple[int, int]] = {
        col: (ri, ci)
        for ri, row in enumerate(numeric_keypad_strs)
        for ci, col in enumerate(row)
    }
    dir_keypad_strs: list[str] = ["G^A", "<v>"]
    dir_keypad: dict[str, tuple[int, int]] = {
        col: (ri, ci)
        for ri, row in enumerate(dir_keypad_strs)
        for ci, col in enumerate(row)
    }
    return numeric_keypad, dir_keypad


def get_dist_and_increment(loc: int, other_loc: int) -> tuple[int, int]:
    dist = other_loc - loc
    dir = 1 if dist >= 0 else -1

    return dist, dir


def is_valid_path(
    path_steps: tuple[str, ...], start_loc: tuple[int, int], gap_loc: tuple[int, int]
) -> bool:
    cur_ri, cur_ci = start_loc
    for step in path_steps:
        if step == "^":
            next_step = (cur_ri - 1, cur_ci)
        elif step == ">":
            next_step = (cur_ri, cur_ci + 1)
        elif step == "v":
            next_step = (cur_ri + 1, cur_ci)
        elif step == "<":
            next_step = (cur_ri, cur_ci - 1)
        else:
            raise ValueError(f"Invalid Path Character: {step}")
        if next_step == gap_loc:
            return False
        cur_ri, cur_ci = next_step
    return True


def consecutive_characters(s: Sequence[str]) -> int:
    if not s or len(s) <= 1:
        return 0
    consecutive: int = 0
    last_seen_char = s[0]
    for i in range(1, len(s)):
        if s[i] == last_seen_char:
            consecutive += 1
        last_seen_char = s[i]
    return consecutive


def gen_single_path(
    start: tuple[int, int], goal: tuple[int, int], gap: tuple[int, int]
) -> list[list[str]]:
    cur_ri, cur_ci = start
    goal_ri, goal_ci = goal
    r_dist, _ = get_dist_and_increment(cur_ri, goal_ri)
    c_dist, _ = get_dist_and_increment(cur_ci, goal_ci)
    row_chars: list[str] = ["^"] * abs(r_dist) if r_dist < 0 else ["v"] * r_dist
    col_chars: list[str] = ["<"] * abs(c_dist) if c_dist < 0 else [">"] * c_dist
    path_chars: list[str] = row_chars + col_chars
    paths_by_consec_chars: dict[int, list[list[str]]] = {}
    for path in set(permutations(path_chars)):
        if not is_valid_path(path, (cur_ri, cur_ci), gap):
            continue
        path_list = list(path)
        path_list.append("A")
        consec_chars = consecutive_characters(path)
        consec_chars_val_list = paths_by_consec_chars.setdefault(consec_chars, [])
        consec_chars_val_list.append(path_list)

    num_most_consec = max(paths_by_consec_chars.keys())

    return paths_by_consec_chars[num_most_consec]


def gen_path(code: str, keypad: dict[str, tuple[int, int]]) -> list[str]:
    goal_sets: list[list[list[str]]] = []
    cur_ri, cur_ci = keypad["A"]

    for goal in code:
        best_paths = gen_single_path((cur_ri, cur_ci), keypad[goal], keypad["G"])
        goal_sets.append(best_paths)
        cur_ri, cur_ci = keypad[goal]

    cartesian_product = product(*goal_sets)
    shortest_paths: list[str] = []
    for path in cartesian_product:
        shortest_paths.append("".join([step for pos in path for step in pos]))
    return shortest_paths


def get_keypresses(
    path: str, keypad: dict[str, tuple[int, int]], to_keypad: dict[str, tuple[int, int]]
) -> str:
    rev_to_keypad: dict[tuple[int, int], str] = {v: k for k, v in to_keypad.items()}
    activations: list[str] = []
    cur_ri, cur_ci = to_keypad["A"]
    for step in path:
        if step == "<":
            cur_ci -= 1
        elif step == "^":
            cur_ri -= 1
        elif step == ">":
            cur_ci += 1
        elif step == "v":
            cur_ri += 1
        elif step == "A":
            activations.append(rev_to_keypad[(cur_ri, cur_ci)])
    return "".join(activations)


def part_one(codes: list[str]) -> int:
    numeric_keypad, dir_keypad = generate_keypads()

    code_paths: dict[str, int] = {}
    for code in codes:
        numeric_path = gen_path(code, numeric_keypad)
        tier_one_paths: list[str] = []
        for path in numeric_path:
            tier_one_paths += gen_path(path, dir_keypad)
        tier_two_paths: list[str] = []
        for path in tier_one_paths:
            tier_two_paths += gen_path(path, dir_keypad)
        min_length = min([len(path) for path in tier_two_paths])
        code_paths[code] = min_length

    complexity = 0
    for code in code_paths:
        cp_len = code_paths[code]
        numeric_portion = int(code[:-1])
        print(f"{code}: {cp_len} * {numeric_portion}")
        complexity += cp_len * numeric_portion

    return complexity


def part_two(codes: list[str]) -> int:
    numeric_keypad, dir_keypad = generate_keypads()

    @cache
    def num_button_presses(start: str, goal: str, level: int) -> int:
        keypad = (
            numeric_keypad
            if start in numeric_keypad and goal in numeric_keypad
            else dir_keypad
        )
        start_pos = keypad[start]
        goal_pos = keypad[goal]
        gap = keypad["G"]
        paths = gen_single_path(start_pos, goal_pos, gap)

        if level == 1:
            return min([len(p) for p in paths])

        current = "A"
        path_presses: list[int] = []
        for path in paths:
            num_presses = 0
            for goal in path:
                keypad = (
                    numeric_keypad
                    if current in numeric_keypad and goal in numeric_keypad
                    else dir_keypad
                )
                goal_pos = keypad[goal]
                num_presses += num_button_presses(current, goal, level - 1)
                current = goal
            path_presses.append(num_presses)

        return min(path_presses)

    code_lengths: dict[str, int] = {}
    num_presses = 0
    cur_pos = "A"
    for code in codes:
        for goal in code:
            num_presses += num_button_presses(cur_pos, goal, 26)
            cur_pos = goal
        code_lengths[code] = num_presses
        num_presses = 0

    complexity = 0
    for code in code_lengths:
        cp_len = code_lengths[code]
        numeric_portion = int(code[:-1])
        print(f"{code}: {cp_len} * {numeric_portion}")
        complexity += cp_len * numeric_portion

    return complexity


def main():
    codes = parse_input()
    print("Part One:")
    print(part_one(codes))
    print("Part Two:")
    print(part_two(codes))


if __name__ == "__main__":
    main()
