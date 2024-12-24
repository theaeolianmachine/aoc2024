import re
from collections import deque
from dataclasses import dataclass
from enum import Enum


class Operation(Enum):
    AND = 1
    OR = 2
    XOR = 3

    @classmethod
    def str_to_op(cls, op: str):
        if op == "AND":
            return cls.AND
        elif op == "OR":
            return cls.OR
        elif op == "XOR":
            return cls.XOR
        else:
            raise ValueError(f"Invalid Operation Name: {op}")


@dataclass
class Gate:
    left: str
    right: str
    op: Operation


def parse_input() -> tuple[dict[str, int], dict[str, Gate]]:
    wire_regex = re.compile(r"(?P<wire>[a-zA-Z0-9]{3}): (?P<val>\d)")
    gate_regex = re.compile(
        r"(?P<left>[a-zA-Z0-9]{3}) (?P<op>[a-zA-Z]{2,3}) (?P<right>[a-zA-Z0-9]{3}) -> (?P<out>[a-zA-Z0-9]{3})"
    )
    wires: dict[str, int] = {}
    wires_to_gates: dict[str, Gate] = {}
    with open("day24/day24.txt") as fobj:
        lines = fobj.readlines()

    for line in lines:
        wire_match = wire_regex.match(line)
        if wire_match:
            wires[wire_match.group("wire")] = int(wire_match.group("val"))
        else:
            gate_match = gate_regex.match(line)
            if not gate_match:
                continue
            wires_to_gates[gate_match.group("out")] = Gate(
                gate_match.group("left"),
                gate_match.group("right"),
                Operation.str_to_op(gate_match.group("op")),
            )

    return wires, wires_to_gates


def build_adj_lists(all_wires: set[str], wires_to_gates: dict[str, Gate]):
    wire_adjacents: dict[str, set[str]] = {wire: set() for wire in all_wires}

    for wire in wires_to_gates:
        gate = wires_to_gates[wire]
        left_set = wire_adjacents.setdefault(gate.left, set())
        left_set.add(wire)
        right_set = wire_adjacents.setdefault(gate.right, set())
        right_set.add(wire)

    return wire_adjacents


def topological_sort(all_wires: set[str], wire_adjacents: dict[str, set[str]]):
    topological_wire_order: list[str] = []
    incoming_degrees: dict[str, int] = {wire: 0 for wire in all_wires}

    for start_vertex in wire_adjacents:
        for end_vertex in wire_adjacents[start_vertex]:
            incoming_degrees[end_vertex] += 1

    nodes_to_visit: deque[str] = deque(
        [node for node in incoming_degrees if incoming_degrees[node] == 0]
    )

    while nodes_to_visit:
        current_node = nodes_to_visit.popleft()
        topological_wire_order.append(current_node)

        for neighbor in wire_adjacents[current_node]:
            incoming_degrees[neighbor] -= 1
            if incoming_degrees[neighbor] == 0:
                nodes_to_visit.append(neighbor)

    if len(topological_wire_order) == len(all_wires):
        return topological_wire_order
    else:
        raise ValueError("Graph has a cycle, impossible to have a topological sort")


def part_one(wires: dict[str, int], wires_to_gates: dict[str, Gate]):
    all_wires: set[str] = set()
    all_wires.update(wires.keys())
    all_wires.update(wires_to_gates.keys())

    wire_adjacents: dict[str, set[str]] = build_adj_lists(all_wires, wires_to_gates)

    topological_wire_order = topological_sort(all_wires, wire_adjacents)

    for wire in topological_wire_order:
        if wire in wires:
            # Value is already set, moving along
            continue
        gate = wires_to_gates[wire]
        left = wires[gate.left]
        right = wires[gate.right]
        if gate.op is Operation.AND:
            wires[wire] = left & right
        elif gate.op is Operation.OR:
            wires[wire] = left | right
        elif gate.op is Operation.XOR:
            wires[wire] = left ^ right
        else:
            raise ValueError(f"Invalid Operation Type: {gate.op}")

    z_outputs = reversed(sorted([wire for wire in wires if wire.startswith("z")]))
    z_binary = "".join([str(wires[z]) for z in z_outputs])
    return int(z_binary, base=2)


def is_input(wire: str) -> bool:
    return wire.startswith("x") or wire.startswith("y")


def is_output(wire: str) -> bool:
    return wire.startswith("z")


def is_input_or_output(wire: str) -> bool:
    return is_output(wire)


def part_two(wires: dict[str, int], wires_to_gates: dict[str, Gate]):
    # Inputs: A, B, C_in
    # Outputs: S, C_out
    # S = A XOR B XOR C_in
    # C_out = (A AND B) OR (C_in AND (A XOR B))

    z_msb = f"z{len([key for key in wires_to_gates if key.startswith("z")]) - 1:02}"
    z_msb = f"z{len([key for key in wires_to_gates if key.startswith("z")]) - 1:02}"
    z_outputs = [key for key in wires_to_gates.keys() if key.startswith("z")]
    z_outputs.sort()
    bad_outputs: set[str] = set()
    for z_output in z_outputs:
        if z_output != z_msb and wires_to_gates[z_output].op is not Operation.XOR:
            bad_outputs.add(z_output)

    # Last bit is a carry, so it should be an OR
    if wires_to_gates[z_msb].op != Operation.OR:
        bad_outputs.add(z_msb)

    # All intermediate calculations must be AND or OR, but not XOR
    for wire, gate in wires_to_gates.items():
        if wire.startswith("z"):
            # We've already checked outputs previously
            continue
        if is_input(gate.left) or is_input(gate.right):
            # Input values can be XOR'd to start intermediate calculations
            continue
        if gate.op is Operation.XOR:
            bad_outputs.add(wire)

    xor_gates = {
        wire: gate for wire, gate in wires_to_gates.items() if gate.op is Operation.XOR
    }
    and_gates = {
        wire: gate for wire, gate in wires_to_gates.items() if gate.op is Operation.AND
    }
    or_gates = {
        wire: gate for wire, gate in wires_to_gates.items() if gate.op is Operation.OR
    }

    # XOR Gates must be used in future XOR gates (for calculation of the SUM bit)
    for xor_gate in xor_gates:
        if is_output(xor_gate):
            # Outputs won't be used again
            continue
        inputs_with_gate = {g.left for g in xor_gates.values()} | {
            g.right for g in xor_gates.values()
        }
        if xor_gate not in inputs_with_gate:
            bad_outputs.add(xor_gate)

    # AND Gates must be used in future OR gates (for calculation of the CARRY bit)
    for and_gate in and_gates:
        if is_output(and_gate):
            # Outputs won't be used again
            continue
        if and_gates[and_gate].left in ("x00", "y00") and and_gates[and_gate].right in (
            "x00",
            "y00",
        ):
            # The first bit is a half adder, so will be immediately AND'ed because it's the carry bit
            # for the half adder
            continue
        inputs_with_gate = {g.left for g in or_gates.values()} | {
            g.right for g in or_gates.values()
        }
        if and_gate not in inputs_with_gate:
            bad_outputs.add(and_gate)

    return ",".join(sorted(bad_outputs))


def main():
    wires, wires_to_gates = parse_input()
    print("Part One:")
    print(part_one(wires, wires_to_gates))
    print("Part Two:")
    print(part_two(wires, wires_to_gates))


if __name__ == "__main__":
    main()
