from dataclasses import dataclass


@dataclass
class Memory:
    reg_a: int
    reg_b: int
    reg_c: int
    inst_ptr: int = 0

    def _combo_operand(self, operand: int) -> int:
        if operand >= 0 and operand <= 3:
            return operand
        elif operand == 4:
            return self.reg_a
        elif operand == 5:
            return self.reg_b
        elif operand == 6:
            return self.reg_c
        else:
            raise ValueError(f"Invalid combo operand: {operand}")

    def _registers_str(self) -> str:
        return f"A: {self.reg_a:#o} B: {self.reg_b:#o} C: {self.reg_c:#o}"

    def print_operation(self, opcode: int, operand: int):
        info_strs = [f"Instruction: {self.inst_ptr}", self._registers_str()]
        if opcode == 0:
            info_strs.append(
                f"adv: A = {self.reg_a:#o} / 2 ** {self._combo_operand(operand)} [{operand}]"
            )
        elif opcode == 1:
            info_strs.append(f"bxl: B = {self.reg_b:#o} ^ {operand}")
        elif opcode == 2:
            info_strs.append(
                f"bst: B = {self._combo_operand(operand):#o} [{operand}] % 8"
            )
        elif opcode == 3:
            info_strs.append(f"jnz: Instruction Pointer = {operand}")
        elif opcode == 4:
            info_strs.append(f"bxc: B = {self.reg_b:#o} ^ {self.reg_c:#o}")
        elif opcode == 5:
            info_strs.append(f"out: {self._combo_operand(operand)} [{operand}] % 8")
        elif opcode == 6:
            info_strs.append(
                f"bdv: B = {self.reg_a:#o} / 2 ** {self._combo_operand(operand)} [{operand}]"
            )
        elif opcode == 7:
            info_strs.append(
                f"cdv: C = {self.reg_a:#o} / 2 ** {self._combo_operand(operand)} [{operand}]"
            )
        print(" ".join(info_strs))

    def adv(self, operand: int):
        """Opcode: 0, performs division with reg_a = reg_a / 2 ** combo_operand."""
        combo_operand: int = self._combo_operand(operand)
        self.reg_a = int(self.reg_a / (2**combo_operand))

    def bxl(self, operand: int):
        """Opcode 1: Calculates bitwise XOR of reg_b = reg_b ^ literal_operand"""
        self.reg_b ^= operand

    def bst(self, operand: int):
        """Opcode 2: Calculates reg_b = combo_operand % 8"""
        combo_operand: int = self._combo_operand(operand)
        self.reg_b = combo_operand % 8

    def jnz(self, operand: int) -> bool:
        """Opcode 3: Jump to instruction #operand if reg_a != 0.

        Instruction pointer should not increment by two.
        """
        if self.reg_a == 0:
            return False
        self.inst_ptr = operand
        return True

    def bxc(self, _: int):
        """Opcode 4: Set reg_b = b ^ c. Operand is ignored."""
        self.reg_b ^= self.reg_c

    def out(self, operand: int) -> str:
        """Opcode 5: Returns combo_operand % 8"""
        combo_operand = self._combo_operand(operand)
        return str(combo_operand % 8)

    def bdv(self, operand: int):
        """Opcode 6: Performs division with reg_b = reg_a / 2 ** combo_operand."""
        combo_operand: int = self._combo_operand(operand)
        self.reg_b = int(self.reg_a / (2**combo_operand))

    def cdv(self, operand: int):
        """Opcode 7: Performs division with reg_c = reg_a / 2 ** combo_operand."""
        combo_operand: int = self._combo_operand(operand)
        self.reg_c = int(self.reg_a / (2**combo_operand))


def parse_input() -> tuple[Memory, list[tuple[int, int]]]:
    with open("day17/day17.txt") as fobj:
        lines = fobj.read().split("\n")

    reg_a: int = int(lines[0][lines[0].find(":") + 1 :])
    reg_b: int = int(lines[1][lines[1].find(":") + 1 :])
    reg_c: int = int(lines[2][lines[2].find(":") + 1 :])
    program_str: list[str] = lines[4][lines[4].find(":") + 1 :].split(",")
    program: list[tuple[int, int]] = []
    for i in range(0, len(program_str), 2):
        program.append((int(program_str[i]), int(program_str[i + 1])))

    return Memory(reg_a, reg_b, reg_c), program


def part_one(memory: Memory, program: list[tuple[int, int]], debug=False) -> str:
    output: list[str] = []
    while memory.inst_ptr >= 0 and memory.inst_ptr < len(program):
        op, operand = program[memory.inst_ptr]
        if debug:
            memory.print_operation(op, operand)
        if op == 0:
            memory.adv(operand)
        elif op == 1:
            memory.bxl(operand)
        elif op == 2:
            memory.bst(operand)
        elif op == 3:
            jumped = memory.jnz(operand)
            if jumped:
                continue
        elif op == 4:
            memory.bxc(operand)
        elif op == 5:
            output.append(memory.out(operand))
        elif op == 6:
            memory.bdv(operand)
        elif op == 7:
            memory.cdv(operand)
        else:
            raise ValueError(f"Invalid Opcode: {op}, {operand}")
        memory.inst_ptr += 1
    return ",".join(output)


def part_two(original_memory: Memory, program: list[tuple[int, int]]):
    program_data: list[str] = []
    for op, operand in program:
        program_data.append(str(op))
        program_data.append(str(operand))

    solutions: list[int] = []

    def backtrack(partial_solution: str, solution_index: int):
        if solution_index == -1:
            solutions.append(int(partial_solution, base=8))
            return

        further_solutions = [f"{partial_solution}{i}" for i in range(8)]
        for candidate in further_solutions:
            memory = Memory(
                int(candidate, base=8), original_memory.reg_b, original_memory.reg_c
            )
            output = part_one(memory, program)
            if output == ",".join(program_data[solution_index:]):
                backtrack(candidate, solution_index - 1)

    backtrack("", len(program_data) - 1)

    return min(solutions)


def main():
    """
    while A != 0:
        B = A % 8
        B ^= 3
        C = A / 2
        B ^= 5
        A = A / 8
        B = B ^ C
        Out(B % 8)

    """
    memory, program = parse_input()
    print("Part One:")
    print(part_one(memory, program))
    memory, program = parse_input()
    print("Part Two:")
    print(part_two(memory, program))


if __name__ == "__main__":
    main()
