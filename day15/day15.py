from dataclasses import dataclass
from enum import Enum


class ItemType(Enum):
    ROBOT = 1
    BOX = 2
    BOX_LEFT = 3
    BOX_RIGHT = 4
    WALL = 5


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


@dataclass
class WarehouseItem:
    row: int
    col: int
    item_type: ItemType


@dataclass
class Warehouse:
    items: dict[tuple[int, int], ItemType]
    rlen: int
    clen: int

    def in_bounds(self, ri: int, ci: int) -> bool:
        return ri >= 0 and ri < self.rlen and ci >= 0 and ci < self.clen

    def print_warehouse(self):
        for ri in range(self.rlen):
            row = []
            for ci in range(self.clen):
                if (ri, ci) not in self.items:
                    row.append(".")
                elif self.items[(ri, ci)] == ItemType.BOX:
                    row.append("O")
                elif self.items[(ri, ci)] == ItemType.BOX_LEFT:
                    row.append("[")
                elif self.items[(ri, ci)] == ItemType.BOX_RIGHT:
                    row.append("]")
                elif self.items[(ri, ci)] == ItemType.ROBOT:
                    row.append("@")
                elif self.items[(ri, ci)] == ItemType.WALL:
                    row.append("#")
            print(*row)


def parse_input(double=False) -> tuple[Warehouse, list[Direction]]:
    warehouse_items: dict[tuple[int, int], ItemType] = {}
    robot_moves: list[Direction] = []

    with open("day15/day15.txt") as fobj:
        lines = fobj.readlines()

    current_line = 0
    matrix_lines = []

    while lines[current_line] != "\n":
        matrix_lines.append(lines[current_line].strip())
        current_line += 1

    for ri, row in enumerate(matrix_lines):
        for ci, col in enumerate(row):
            if col == "#":
                if double:
                    warehouse_items[(ri, ci * 2)] = ItemType.WALL
                    warehouse_items[(ri, ci * 2 + 1)] = ItemType.WALL
                else:
                    warehouse_items[(ri, ci)] = ItemType.WALL
            elif col == "O":
                if double:
                    warehouse_items[(ri, ci * 2)] = ItemType.BOX_LEFT
                    warehouse_items[(ri, ci * 2 + 1)] = ItemType.BOX_RIGHT
                else:
                    warehouse_items[(ri, ci)] = ItemType.BOX
            elif col == "@":
                if double:
                    warehouse_items[(ri, ci * 2)] = ItemType.ROBOT
                else:
                    warehouse_items[(ri, ci)] = ItemType.ROBOT

    robot_moves_str = "".join([line.strip() for line in lines[current_line + 1 :]])
    for char in robot_moves_str:
        if char == "<":
            robot_moves.append(Direction.WEST)
        elif char == "^":
            robot_moves.append(Direction.NORTH)
        elif char == ">":
            robot_moves.append(Direction.EAST)
        elif char == "v":
            robot_moves.append(Direction.SOUTH)
        else:
            raise ValueError(f"Encountered invalid robot move: {char}")

    rlen = len(matrix_lines)
    clen = len(matrix_lines) * 2 if double else len(matrix_lines[0])
    return Warehouse(warehouse_items, rlen, clen), robot_moves


def get_next_position(loc: tuple[int, int], direction: Direction) -> tuple[int, int]:
    if direction == Direction.NORTH:
        return (loc[0] - 1, loc[1])
    elif direction == Direction.EAST:
        return (loc[0], loc[1] + 1)
    elif direction == Direction.SOUTH:
        return (loc[0] + 1, loc[1])
    elif direction == Direction.WEST:
        return (loc[0], loc[1] - 1)
    else:
        raise ValueError("Invalid Direction")


def get_direction_increment(direction: Direction) -> tuple[int, int]:
    if direction == Direction.NORTH:
        return (-1, 0)
    elif direction == Direction.EAST:
        return (0, 1)
    elif direction == Direction.SOUTH:
        return (1, 0)
    elif direction == Direction.WEST:
        return (0, -1)
    else:
        raise ValueError("Invalid Direction")


def get_consecutive_boxes(
    starting_pos: tuple[int, int], move_dir: Direction, warehouse: Warehouse
) -> list[tuple[int, int]]:
    consecutive_boxes: list[tuple[int, int]] = [starting_pos]
    row_inc, col_inc = get_direction_increment(move_dir)
    row = starting_pos[0] + row_inc
    col = starting_pos[1] + col_inc
    while (
        warehouse.in_bounds(row, col)
        and (row, col) in warehouse.items
        and warehouse.items[(row, col)] == ItemType.BOX
    ):
        consecutive_boxes.append((row, col))
        row += row_inc
        col += col_inc

    return consecutive_boxes


def get_double_pair(
    pos: tuple[int, int], box_type: ItemType
) -> tuple[tuple[int, int], tuple[int, int]]:
    if box_type == ItemType.BOX_RIGHT:
        return ((pos[0], pos[1] - 1), pos)
    elif box_type == ItemType.BOX_LEFT:
        return (pos, (pos[0], pos[1] + 1))
    else:
        raise ValueError("Invalid Item Type (Not a Box)")


def get_double_consecutive_boxes(
    starting_pos: tuple[int, int],
    move_dir: Direction,
    warehouse: Warehouse,
) -> set[tuple[tuple[int, int], tuple[int, int]]]:
    box_type = warehouse.items[starting_pos]
    starting_pair = get_double_pair(starting_pos, box_type)
    consecutive_boxes: set[tuple[tuple[int, int], tuple[int, int]]] = {starting_pair}
    row_inc, col_inc = get_direction_increment(move_dir)
    if move_dir in (Direction.EAST, Direction.WEST):
        row = starting_pos[0] + (row_inc * 2)
        col = starting_pos[1] + (col_inc * 2)
        while (
            warehouse.in_bounds(row, col)
            and (row, col) in warehouse.items
            and warehouse.items[(row, col)] == box_type
        ):
            if move_dir == Direction.EAST:
                next_box = ((row, col), (row + row_inc, col + col_inc))
            else:
                next_box = ((row + row_inc, col + col_inc), (row, col))
            consecutive_boxes.add(next_box)
            row += row_inc * 2
            col += col_inc * 2

    elif move_dir in (Direction.NORTH, Direction.SOUTH):
        # Two cases: where it's aligned with a single box, or it's in a position to push two boxes
        next_left = (starting_pair[0][0] + row_inc, starting_pair[0][1] + col_inc)
        next_right = (starting_pair[1][0] + row_inc, starting_pair[1][1] + col_inc)
        positions_to_check: set[tuple[tuple[int, int], tuple[int, int]]] = set(
            ((next_left, next_right),)
        )
        while positions_to_check:
            next_left, next_right = positions_to_check.pop()
            if (
                next_left in warehouse.items
                and warehouse.items[next_left] == ItemType.WALL
            ) or (
                next_right in warehouse.items
                and warehouse.items[next_right] == ItemType.WALL
            ):
                # We've hit a wall
                return set()
            if (
                warehouse.in_bounds(*next_left)
                and next_left in warehouse.items
                and warehouse.items[next_left]
                in (ItemType.BOX_LEFT, ItemType.BOX_RIGHT)
            ):
                left_box = get_double_pair(next_left, warehouse.items[next_left])
                consecutive_boxes.add(left_box)
                positions_to_check.add(
                    (
                        (left_box[0][0] + row_inc, left_box[0][1] + col_inc),
                        (left_box[1][0] + row_inc, left_box[1][1] + col_inc),
                    )
                )
            if (
                warehouse.in_bounds(*next_right)
                and next_right in warehouse.items
                and warehouse.items[next_right]
                in (ItemType.BOX_LEFT, ItemType.BOX_RIGHT)
            ):
                right_box = get_double_pair(next_right, warehouse.items[next_right])
                consecutive_boxes.add(right_box)
                positions_to_check.add(
                    (
                        (right_box[0][0] + row_inc, right_box[0][1] + col_inc),
                        (right_box[1][0] + row_inc, right_box[1][1] + col_inc),
                    )
                )

    return consecutive_boxes


def get_double_box_boundary(
    consecutive_boxes: set[tuple[tuple[int, int], tuple[int, int]]], dir: Direction
) -> list[tuple[int, int]]:
    boundaries: list[tuple[int, int]] = []
    if dir == Direction.NORTH:
        furthest = min(left[0] for left, _ in consecutive_boxes)
        for left, right in consecutive_boxes:
            if left[0] == furthest:
                boundaries.append(left)
                boundaries.append(right)
    elif dir == Direction.EAST:
        furthest = max(right[1] for _, right in consecutive_boxes)
        for _, right in consecutive_boxes:
            if right[1] == furthest:
                boundaries.append(right)
    elif dir == Direction.SOUTH:
        furthest = max(left[0] for left, _ in consecutive_boxes)
        for left, right in consecutive_boxes:
            if left[0] == furthest:
                boundaries.append(left)
                boundaries.append(right)
    elif dir == Direction.WEST:
        furthest = min(left[1] for left, _ in consecutive_boxes)
        for left, _ in consecutive_boxes:
            if left[1] == furthest:
                boundaries.append(left)
    else:
        raise ValueError("Invalid Direction")
    return boundaries


def part_one(warehouse: Warehouse, robot_moves: list[Direction]):
    """
    Look into the direction of the movement.
    If it's a wall, nothing happens, the move is skipped.
    If it's empty, the robot moves to the new location.
    If it's a box, find all consecutive boxes in the direction of movement. If one space over in the direction
    of movement contains an empty space, move all consecutive items over one space, and move the robot over one space.
    If it contains a wall, no movement occurs, the move is skipped.
    """
    robot_loc = [
        loc for loc, item in warehouse.items.items() if item == ItemType.ROBOT
    ][0]
    for move_dir in robot_moves:
        next_position = get_next_position(robot_loc, move_dir)
        if not warehouse.in_bounds(*next_position):
            # Next move would be out of bounds
            continue
        elif next_position not in warehouse.items:
            # Next move is an empty space
            del warehouse.items[robot_loc]
            robot_loc = next_position
            warehouse.items[robot_loc] = ItemType.ROBOT
        elif warehouse.items[next_position] == ItemType.WALL:
            # Nothing happens when you run into a wall
            continue
        elif warehouse.items[next_position] == ItemType.BOX:
            consecutive_boxes = get_consecutive_boxes(
                next_position, move_dir, warehouse
            )
            row_inc, col_inc = get_direction_increment(move_dir)
            pos_after_boxes = (
                consecutive_boxes[-1][0] + row_inc,
                consecutive_boxes[-1][1] + col_inc,
            )
            if (
                warehouse.in_bounds(*pos_after_boxes)
                and pos_after_boxes not in warehouse.items
            ):
                # Next space is empty, let's move everything over
                for box_loc in consecutive_boxes:
                    del warehouse.items[box_loc]
                new_locs = [
                    (ri + row_inc, ci + col_inc) for ri, ci in consecutive_boxes
                ]
                for loc in new_locs:
                    warehouse.items[loc] = ItemType.BOX

                # Move the robot after shifting the boxes
                del warehouse.items[robot_loc]
                robot_loc = next_position
                warehouse.items[robot_loc] = ItemType.ROBOT

    box_gps = [
        (loc[0] * 100) + loc[1]
        for loc, item_type in warehouse.items.items()
        if item_type == ItemType.BOX
    ]

    return sum(box_gps)


def part_two(warehouse: Warehouse, robot_moves):
    """
    Look into the direction of the movement.
    If it's a wall, nothing happens, the move is skipped.
    If it's empty, the robot moves to the new location.
    If it's a box, find all consecutive boxes in the direction of movement. If one space over in the direction
    of movement contains an empty space, move all consecutive items over one space, and move the robot over one space.
    If it contains a wall, no movement occurs, the move is skipped.
    """
    robot_loc = [
        loc for loc, item in warehouse.items.items() if item == ItemType.ROBOT
    ][0]
    gps_scores: list[int] = []
    for i, move_dir in enumerate(robot_moves):
        next_position = get_next_position(robot_loc, move_dir)
        if not warehouse.in_bounds(*next_position):
            # Next move would be out of bounds
            gps_score = sum(
                [
                    (left_box[0] * 100) + left_box[1]
                    for left_box in warehouse.items
                    if warehouse.items[left_box] == ItemType.BOX_LEFT
                ]
            )
            gps_scores.append(gps_score)
            continue
        elif next_position not in warehouse.items:
            # Next move is an empty space
            del warehouse.items[robot_loc]
            robot_loc = next_position
            warehouse.items[robot_loc] = ItemType.ROBOT
        elif warehouse.items[next_position] == ItemType.WALL:
            # Nothing happens when you run into a wall
            gps_score = sum(
                [
                    (left_box[0] * 100) + left_box[1]
                    for left_box in warehouse.items
                    if warehouse.items[left_box] == ItemType.BOX_LEFT
                ]
            )
            gps_scores.append(gps_score)
            continue
        elif warehouse.items[next_position] in (ItemType.BOX_LEFT, ItemType.BOX_RIGHT):
            # The same rules apply when going east or west, this is because a box is always
            # in a horizontal orientation
            # The edge case applies when you're going north or south when considering adjacent boxes.
            # Adjacency is also matched by the same edge, i.e. match on BOX_RIGHT when going WEST
            # and count by 2 instead of one.
            consecutive_boxes = get_double_consecutive_boxes(
                next_position, move_dir, warehouse
            )
            if not consecutive_boxes:
                # We hit a wall
                continue
            row_inc, col_inc = get_direction_increment(move_dir)
            pos_after_boxes = [
                (ri + row_inc, ci + col_inc)
                for ri, ci in get_double_box_boundary(consecutive_boxes, move_dir)
            ]
            all_in_bounds = all(
                warehouse.in_bounds(ri, ci) for ri, ci in pos_after_boxes
            )
            all_empty = all(pos not in warehouse.items for pos in pos_after_boxes)
            if all_in_bounds and all_empty:
                # Next space is empty, let's move everything over
                new_positions: dict[tuple[int, int], ItemType] = {}
                for left, right in consecutive_boxes:
                    new_left = (left[0] + row_inc, left[1] + col_inc)
                    new_right = (right[0] + row_inc, right[1] + col_inc)
                    new_positions[new_left] = ItemType.BOX_LEFT
                    new_positions[new_right] = ItemType.BOX_RIGHT
                    del warehouse.items[left]
                    del warehouse.items[right]

                warehouse.items.update(new_positions)

                # Move the robot after shifting the boxes
                del warehouse.items[robot_loc]
                robot_loc = next_position
                warehouse.items[robot_loc] = ItemType.ROBOT

    box_gps = [
        (left_box[0] * 100) + left_box[1]
        for left_box in warehouse.items
        if warehouse.items[left_box] == ItemType.BOX_LEFT
    ]

    return sum(box_gps)


def main():
    warehouse, robot_moves = parse_input()
    print("Part One:")
    print(part_one(warehouse, robot_moves))
    warehouse, robot_moves = parse_input(double=True)
    print("Part Two:")
    print(part_two(warehouse, robot_moves))


if __name__ == "__main__":
    main()
