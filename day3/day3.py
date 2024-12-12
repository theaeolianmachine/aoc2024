import re


def parse_input() -> list[str]:
    with open("day3/day3.txt") as fobj:
        return fobj.readlines()


def part_one(instructions: list[str]):
    mul_regex = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    total_sum = 0

    for line in instructions:
        matches = mul_regex.findall(line)
        total_sum += sum([int(match[0]) * int(match[1]) for match in matches])

    return total_sum


def part_two(instructions: list[str]):
    do_regex = re.compile(r"do\(\)")
    dont_regex = re.compile(r"don't\(\)")
    mul_regex = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    total_sum = 0

    inst_str = "\n".join(instructions)

    do_end_indexes = [match.end() for match in do_regex.finditer(inst_str)]
    dont_end_indexes = [match.end() for match in dont_regex.finditer(inst_str)]
    regions = find_enabled_regions(do_end_indexes, dont_end_indexes)
    print(regions)

    for region in regions:
        line_slice = (
            inst_str[region[0] : region[1]] if region[1] > 0 else inst_str[region[0] :]
        )
        total_sum += get_muls_in_region(line_slice, mul_regex)

    return total_sum


def get_muls_in_region(line: str, mul_regex: re.Pattern) -> int:
    return sum(
        [
            int(match.group(1)) * int(match.group(2))
            for match in mul_regex.finditer(line)
        ]
    )


def find_enabled_regions(do_indexes: list[int], dont_indexes: list[int]):
    do_dont_dict: dict[int, bool] = {}
    for i in do_indexes:
        do_dont_dict[i] = True

    for i in dont_indexes:
        do_dont_dict[i] = False

    regions: list[tuple[int, int]] = []

    region_start: int | None = 0

    for i in sorted(do_dont_dict.keys()):
        if do_dont_dict[i] and region_start is not None:
            # Enabled, saw another enable
            continue
        elif region_start is None and not do_dont_dict[i]:
            # Disabled, saw another disable
            continue
        elif region_start is not None and not do_dont_dict[i]:
            # Enabled, saw a disable
            regions.append((region_start, i))
            region_start = None
        elif region_start is None and do_dont_dict[i]:
            # Disabled, saw an enable
            region_start = i

    if region_start is not None:
        regions.append((region_start, -1))

    return regions


def main():
    instructions: list[str] = parse_input()
    print("Part One:")
    print(part_one(instructions))
    print("Part Two:")
    print(part_two(instructions))


if __name__ == "__main__":
    main()
