from itertools import combinations


def parse_input() -> dict[str, set[str]]:
    with open("day23/day23.txt") as fobj:
        lines = fobj.readlines()

    connection_pairs = [line.strip().split("-") for line in lines]
    connections: dict[str, set[str]] = {}
    for pair in connection_pairs:
        left, right = (pair[0], pair[1])
        left_conns = connections.setdefault(left, set())
        left_conns.add(right)
        right_conns = connections.setdefault(right, set())
        right_conns.add(left)

    return connections


def part_one(connections: dict[str, set[str]]):
    computer_trios: set[tuple[str, ...]] = set()
    for conn in connections:
        for left, right in combinations(connections[conn], 2):
            computer_starts_with_t = any(
                computer.startswith("t") for computer in (conn, left, right)
            )
            if not computer_starts_with_t:
                continue
            potential_trio = tuple(sorted([conn, left, right]))
            if potential_trio in computer_trios:
                # We've already added this trio
                continue
            if right in connections[left]:
                computer_trios.add(tuple(sorted([conn, left, right])))

    return len(computer_trios)


def part_two(connections: dict[str, set[str]]):
    lan_party_size = max(len(connections[pair]) for pair in connections) + 1
    while lan_party_size > 0:
        for conn in connections:
            if len(connections[conn]) < lan_party_size:
                # We'll come back to you, but currently biggest party would not work.
                continue
            for combo in combinations(connections[conn], lan_party_size):
                lan_party = set(combo)
                lan_party.add(conn)
                all_members_share_connection = all(
                    [
                        (connections[combo_conn] | {combo_conn}) >= lan_party
                        for combo_conn in combo
                    ]
                )
                if all_members_share_connection:
                    return ",".join(sorted(lan_party))
        # Look for a smaller party
        lan_party_size -= 1

    # Could the LAN party
    return []


def main():
    problem_input = parse_input()
    print("Part One:")
    print(part_one(problem_input))
    print("Part Two:")
    print(part_two(problem_input))


if __name__ == "__main__":
    main()
