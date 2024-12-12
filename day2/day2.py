def parse_reports() -> list[tuple[int, ...]]:
    with open("day2/day2.txt") as fobj:
        lines = fobj.readlines()

    return [tuple(int(num) for num in line.strip().split()) for line in lines]


def part_one(reports: list[tuple[int, ...]]):
    safe_reports = [report for report in reports if is_report_safe(report)]
    return len(safe_reports)


def part_two(reports: list[tuple[int, ...]]):
    num_safe_reports = 0
    for report in reports:
        if is_report_safe(report):
            num_safe_reports += 1
        elif is_dampen_safe(report):
            num_safe_reports += 1

    return num_safe_reports


def is_dampen_safe(unsafe_report: tuple[int, ...]):
    solutions: list[tuple[int, ...]] = []
    for i in range(len(unsafe_report)):
        if i == 0:
            solutions.append(unsafe_report[1:])
        else:
            solutions.append(
                unsafe_report[0:i] + unsafe_report[i + 1 : len(unsafe_report)]
            )

    return any(is_report_safe(sol) for sol in solutions)


def is_report_safe(report: tuple[int, ...]):
    is_asc: bool | None = None

    for i in range(1, len(report), 1):
        level = report[i]
        prev_level = report[i - 1]
        # Always unsafe if levels are the same
        if level == prev_level:
            return False
        if is_asc is None:
            is_asc = level > prev_level
        else:
            check_is_asc = level > prev_level
            # Switched Directions
            if is_asc != check_is_asc:
                return False
        diff = abs(level - prev_level)
        # Level diff is unsafe
        if diff < 1 or diff > 3:
            return False

    # Passed all checks
    return True


def main():
    reports: list[tuple[int, ...]] = parse_reports()
    print("Part One:")
    print(part_one(reports))
    print("Part Two:")
    print(part_two(reports))


if __name__ == "__main__":
    main()
