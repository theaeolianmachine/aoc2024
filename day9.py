def parse_input() -> str:
    with open("day9small.txt") as fobj:
        return fobj.read().strip()


def part_one(file_map: str) -> int:
    # Alternates from back to front, file then free space
    # Forwards is file then free space as well, since it's always odd

    forward_ptr = 0
    forward_fnum = 0
    backward_ptr = len(file_map) - 1
    backward_fnum = len(file_map) // 2
    backward_size = int(file_map[backward_ptr])
    file_locations: dict[int, list[tuple[int, int]]] = {}

    while forward_ptr < backward_ptr:
        # Mark the file on the left
        forward_size = int(file_map[forward_ptr])
        cur_file_locations = file_locations.setdefault(forward_fnum, [])
        cur_file_locations.append(
            (
                forward_ptr,
                forward_ptr + forward_size - 1,
            )
        )
        forward_ptr += 1

        # Defrag in the free space
        free_space_size = int(file_map[forward_ptr])
        cur_file_locations = file_locations.setdefault(backward_fnum, [])

        while free_space_size > 0:
            if free_space_size <= backward_size:
                cur_file_locations.append(
                    (forward_ptr, forward_ptr + free_space_size - 1)
                )
                backward_size -= free_space_size
                free_space_size = 0


def part_two():
    pass


def main():
    file_map = parse_input()
    print("Part One:")
    print(part_one(file_map))
    print("Part Two:")
    print(part_two())


if __name__ == "__main__":
    main()
