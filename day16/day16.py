import heapq
from dataclasses import dataclass
from enum import IntEnum
from typing import Self


class Direction(IntEnum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

    def num_rotations(self, other: Self) -> int:
        num_fields = len(self.__class__)
        forward = (other - self) % num_fields
        backward = (self - other) % num_fields

        return min((forward, backward))


@dataclass(frozen=True, order=True)
class MazeNode:
    ri: int
    ci: int
    dir: Direction


def parse_input():
    with open("day16/day16.txt") as fobj:
        return [[c for c in line] for line in fobj.read().split("\n")]


def valid_adjacent(ri: int, ci: int, maze: list[list[str]]) -> bool:
    return (
        ri >= 0
        and ri < len(maze)
        and ci >= 0
        and ci < len(maze)
        and maze[ri][ci] != "#"
    )


def get_adjacent_nodes(maze_path: MazeNode, maze: list[list[str]]) -> set[MazeNode]:
    all_adjacents: set[MazeNode] = {
        MazeNode(maze_path.ri - 1, maze_path.ci, Direction.NORTH),
        MazeNode(maze_path.ri, maze_path.ci + 1, Direction.EAST),
        MazeNode(maze_path.ri + 1, maze_path.ci, Direction.SOUTH),
        MazeNode(maze_path.ri, maze_path.ci - 1, Direction.WEST),
    }

    return {adj for adj in all_adjacents if valid_adjacent(adj.ri, adj.ci, maze)}


def search_heuristic(maze_node: MazeNode, goal: tuple[int, int]):
    gri, gci = goal
    manhattan_distance = abs(maze_node.ri - gri) + abs(maze_node.ci - gci)
    turn_penalty = 0
    if maze_node.dir == Direction.NORTH:
        if gri > maze_node.ri:
            turn_penalty += 2
        if gci != maze_node.ci:
            turn_penalty += 1
    elif maze_node.dir == Direction.SOUTH:
        if gri < maze_node.ri:
            turn_penalty += 2
        if gci != maze_node.ci:
            turn_penalty += 1
    elif maze_node.dir == Direction.EAST:
        if gri != maze_node.ri:
            turn_penalty += 1
        if gci < maze_node.ci:
            turn_penalty += 2
    elif maze_node.dir == Direction.WEST:
        if gri != maze_node.ri:
            turn_penalty += 1
        if gci > maze_node.ci:
            turn_penalty += 2
    else:
        raise ValueError("Invalid Direction")

    turn_penalty *= 1000
    return manhattan_distance + turn_penalty


def part_one(maze: list[list[str]]):
    start: MazeNode | None = None
    goal: tuple[int, int] | None = None

    for ri in range(len(maze)):
        for ci in range(len(maze[ri])):
            if maze[ri][ci] == "S":
                assert start is None
                start = MazeNode(ri, ci, Direction.EAST)
            if maze[ri][ci] == "E":
                assert goal is None
                goal = (ri, ci)

    if start is None or goal is None:
        raise ValueError("Couldn't find the start or the finish")

    pri_queue: list[tuple[int, MazeNode]] = [(search_heuristic(start, goal), start)]
    parent_nodes: dict[MazeNode, MazeNode] = {}
    g_scores: dict[MazeNode, int] = {start: 0}
    f_scores: dict[MazeNode, int] = {start: search_heuristic(start, goal)}

    while pri_queue:
        f_score, maze_node = heapq.heappop(pri_queue)
        if (maze_node.ri, maze_node.ci) == goal:
            total_score = 0
            current_node = maze_node
            while current_node in parent_nodes:
                parent_node = parent_nodes[current_node]
                total_score += 1 + (
                    1000 * parent_node.dir.num_rotations(current_node.dir)
                )
                current_node = parent_node
            return total_score

        for adj_node in get_adjacent_nodes(maze_node, maze):
            g_score = (
                g_scores[maze_node]
                + (maze_node.dir.num_rotations(adj_node.dir) * 1000)
                + 1
            )
            if adj_node not in g_scores or g_score < g_scores[adj_node]:
                f_score = g_score + search_heuristic(adj_node, goal)
                parent_nodes[adj_node] = maze_node
                g_scores[adj_node] = g_score
                f_scores[adj_node] = f_score
                if adj_node not in pri_queue:
                    heapq.heappush(pri_queue, (f_score, adj_node))

    raise ValueError("Impossible to reach goal")


def part_two():
    pass


def main():
    maze = parse_input()
    print("Part One:")
    print(part_one(maze))
    print("Part Two:")
    print(part_two())


if __name__ == "__main__":
    main()
