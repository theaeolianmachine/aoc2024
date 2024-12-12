from itertools import product


def parse_input() -> list[tuple[int, tuple[int, ...]]]:
    parsed: list[tuple[int, tuple[int, ...]]] = []
    with open("day7/day7.txt") as fobj:
        lines = fobj.readlines()

    for line in lines:
        split = line.strip().split(":")
        test_value = int(split[0])
        operands = tuple(int(val) for val in split[1].strip().split(" "))
        parsed.append((test_value, operands))

    return parsed


def calc_test_value(first_value: int, expression: list[tuple[int, str]]) -> int:
    calc = first_value
    for operand, op in expression:
        if op == "+":
            calc += operand
        elif op == "*":
            calc *= operand
        elif op == "|":
            calc = int(str(calc) + str(operand))
        else:
            raise ValueError("Bad operator")
    return calc


def part_one(equations: list[tuple[int, tuple[int, ...]]]) -> int:
    operators = ("+", "*")
    total_calibration_result = 0
    for equation in equations:
        output, operands = equation
        num_operators = len(operands) - 1
        for perm in list(product(operators, repeat=num_operators)):
            current_calc = operands[0]
            zipped_expression: list[tuple[int, str]] = list(zip(operands[1:], perm))
            test_value = calc_test_value(current_calc, zipped_expression)
            if output == test_value:
                total_calibration_result += output
                break
    return total_calibration_result


def part_two(equations: list[tuple[int, tuple[int, ...]]]) -> int:
    operators = ("+", "*", "|")
    total_calibration_result = 0
    for equation in equations:
        output, operands = equation
        num_operators = len(operands) - 1
        for perm in list(product(operators, repeat=num_operators)):
            current_calc = operands[0]
            zipped_expression: list[tuple[int, str]] = list(zip(operands[1:], perm))
            test_value = calc_test_value(current_calc, zipped_expression)
            if output == test_value:
                total_calibration_result += output
                break
    return total_calibration_result


def main():
    equations = parse_input()
    print("Part One:")
    print(part_one(equations))
    print("Part Two:")
    print(part_two(equations))


if __name__ == "__main__":
    main()
