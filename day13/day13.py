import re
from dataclasses import dataclass


@dataclass
class Prize:
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize_loc: tuple[int, int]


def parse_input() -> list[Prize]:
    prizes: list[Prize] = []
    button_regex = re.compile(r"Button [AB]: X[+](\d+), Y[+](\d+)")
    prize_regex = re.compile(r"Prize: X=(\d+), Y=(\d+)")
    with open("day13/day13.txt") as fobj:
        lines = fobj.readlines()

    for i in range(0, len(lines), 4):
        button_a_match = button_regex.search(lines[i])
        button_b_match = button_regex.search(lines[i + 1])
        prize_loc_match = prize_regex.search(lines[i + 2])

        if button_a_match:
            x, y = (int(val) for val in button_a_match.groups())
            button_a = (x, y)
        else:
            raise ValueError("Couldn't find Button A match")

        if button_b_match:
            x, y = (int(val) for val in button_b_match.groups())
            button_b = (x, y)
        else:
            raise ValueError("Couldn't find Button B match")

        if prize_loc_match:
            x, y = (int(val) for val in prize_loc_match.groups())
            prize_loc = (x, y)
        else:
            raise ValueError("Couldn't find Prize Location match")

        prizes.append(Prize(button_a, button_b, prize_loc))

    return prizes


def part_one(prizes: list[Prize]) -> int:
    """
    Formula:
    xA + yB = P

    xA_x + yB_x = P_x
    xA_y + yB_y = P_y

    y = (P_x - xA_x) / B_x
    y = (P_y - xA_y) / P_y

    """
    tokens_spent: int = 0

    for prize in prizes:
        ax, ay = prize.button_a
        bx, by = prize.button_b
        prize_x, prize_y = prize.prize_loc

        ynum = (prize_x * ay) - (prize_y * ax)
        ydenom = (bx * ay) - (by * ax)

        if ynum % ydenom != 0:
            continue

        y = ynum // ydenom

        xnum = prize_x - (bx * y)
        if xnum % ax != 0:
            continue

        x = xnum // ax

        tokens_spent += (3 * x) + y

    return tokens_spent


def part_two(prizes: list[Prize]) -> int:
    adj: int = 10000000000000
    adj_prizes: list[Prize] = []
    for prize in prizes:
        new_prize = Prize(
            prize.button_a,
            prize.button_b,
            (prize.prize_loc[0] + adj, prize.prize_loc[1] + adj),
        )
        adj_prizes.append(new_prize)
    return part_one(adj_prizes)


def main():
    prizes = parse_input()
    print("Part One:")
    print(part_one(prizes))
    print("Part Two:")
    print(part_two(prizes))


if __name__ == "__main__":
    main()
