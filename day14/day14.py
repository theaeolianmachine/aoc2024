import re
from collections import Counter
from dataclasses import dataclass


@dataclass
class Robot:
    position: tuple[int, int]
    velocity: tuple[int, int]
    bounds: tuple[int, int]

    def _wrap_position(self, axis_position: int, boundary: int):
        if axis_position < 0:
            return boundary + axis_position
        elif axis_position >= boundary:
            return axis_position - boundary
        else:
            return axis_position

    def move(self):
        self.position = (
            self._wrap_position(self.position[0] + self.velocity[0], self.bounds[0]),
            self._wrap_position(self.position[1] + self.velocity[1], self.bounds[1]),
        )

    def quadrant(self):
        middle_x = self.bounds[0] // 2
        middle_y = self.bounds[1] // 2

        x, y = self.position

        if x == middle_x or y == middle_y:
            # Middle, not a quadrant
            return -1
        elif x >= 0 and x < middle_x:
            if y >= 0 and y < middle_y:
                return 0
            else:
                return 1
        else:
            if y >= 0 and y < middle_y:
                return 2
            else:
                return 3


def parse_input():
    bounds = (101, 103)
    # bounds = (11, 7)
    robot_re = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    robots: list[Robot] = []
    with open("day14/day14.txt") as fobj:
        lines = fobj.readlines()

    for line in lines:
        parsed_line = robot_re.findall(line.strip())[0]
        position = (int(parsed_line[0]), int(parsed_line[1]))
        velocity = (int(parsed_line[2]), int(parsed_line[3]))

        robots.append(Robot(position, velocity, bounds))

    return robots


def part_one(robots: list[Robot]):
    safety_factor = 1
    for i in range(100):
        for robot in robots:
            robot.move()

    robots_by_quadrant = Counter(
        robot.quadrant() for robot in robots if robot.quadrant() != -1
    )

    for count in robots_by_quadrant.values():
        safety_factor *= count

    return safety_factor


def high_consecutive_robots(robots: list[Robot], bounds: tuple[int, int]) -> bool:
    bound_x, bound_y = bounds
    grid = []
    for r in range(bound_y):
        row = ["." for _ in range(bound_x)]
        grid.append(row)

    for robot in robots:
        x, y = robot.position
        grid[y][x] = "A"

    for row in grid:
        sections = []
        consecutive = 0
        for col in row:
            if col == "A":
                consecutive += 1
            else:
                sections.append(consecutive)
                consecutive = 0
        if any(section_len >= 15 for section_len in sections):
            return True

    return False


def part_two(robots: list[Robot]):
    bounds = (101, 103)
    for i in range(10000):
        for robot in robots:
            robot.move()
        if high_consecutive_robots(robots, bounds):
            return i + 1


def main():
    robots = parse_input()
    print("Part One:")
    print(part_one(robots))
    robots = parse_input()
    print("Part Two:")
    print(part_two(robots))


if __name__ == "__main__":
    main()
