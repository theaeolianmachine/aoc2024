def parse_input() -> str:
    with open("day9/day9.txt") as fobj:
        return fobj.read().strip()


def part_one(file_map: str) -> int:
    # Alternates from back to front, file then free space
    # Forwards is file then free space as well, since it's always odd

    checksum = 0
    file_index = 0

    forward_ptr = 0
    forward_fnum = 0

    backward_ptr = len(file_map) - 1
    backward_fnum = len(file_map) // 2
    backward_size = int(file_map[backward_ptr])
    file_locations: dict[int, list[tuple[int, int]]] = {}

    while forward_fnum <= backward_fnum:
        # Mark the file on the left
        forward_size = (
            int(file_map[forward_ptr])
            if forward_fnum != backward_fnum
            else backward_size
        )
        cur_file_locations = file_locations.setdefault(forward_fnum, [])
        cur_file_locations.append(
            (
                file_index,
                file_index + forward_size - 1,
            )
        )
        forward_ptr += 1
        forward_fnum += 1
        file_index += forward_size

        # Defrag in the free space
        free_space_size = int(file_map[forward_ptr])
        cur_file_locations = file_locations.setdefault(backward_fnum, [])

        while free_space_size > 0 and backward_fnum >= forward_fnum:
            if free_space_size <= backward_size:
                cur_file_locations.append(
                    (file_index, file_index + free_space_size - 1)
                )
                backward_size -= free_space_size
                file_index += free_space_size
                free_space_size = 0
            else:
                cur_file_locations.append((file_index, file_index + backward_size - 1))
                free_space_size -= backward_size
                file_index += backward_size

                backward_ptr -= 2
                backward_fnum -= 1
                backward_size = int(file_map[backward_ptr])
                cur_file_locations = file_locations.setdefault(backward_fnum, [])

        forward_ptr += 1

    for fnum in sorted(file_locations.keys()):
        franges = file_locations[fnum]
        for start, end in franges:
            checksum += sum([val * fnum for val in range(start, end + 1)])

    return checksum


def part_two(file_map: str) -> int:
    checksum = 0
    fnum = 0
    fpos = 0

    file_locations: dict[int, tuple[int, int]] = {}
    free_space_blocks: dict[int, set[tuple[int, int]]] = {}
    for findex, size in enumerate(file_map):
        size_num = int(size)
        if findex % 2 == 0:
            file_locations[fnum] = (fpos, fpos + size_num)
            fnum += 1
        elif size_num > 0:
            cur_blocks = free_space_blocks.setdefault(size_num, set())
            cur_blocks.add((fpos, fpos + size_num))
        fpos += int(size)

    for fnum in reversed(sorted(file_locations.keys())):
        fsize = file_locations[fnum][1] - file_locations[fnum][0]
        big_enough_block_sizes = {
            size
            for size in free_space_blocks.keys()
            if size >= fsize and free_space_blocks[size]
        }
        if not big_enough_block_sizes:
            continue

        leftmost_loc = min(
            {
                blocks
                for bs in big_enough_block_sizes
                for blocks in free_space_blocks[bs]
            }
        )
        if leftmost_loc[0] > file_locations[fnum][0]:
            # Can't move more leftward
            continue

        leftmost_size = leftmost_loc[1] - leftmost_loc[0]

        # Free block
        # Note that this doesn't merge free blocks, but it doesn't matter
        # because a freed block on the right won't be used by a lower
        # number on the left. It's unnecessary for the answer as well,
        # but it made printing and debugging easier.
        freed_block = free_space_blocks.setdefault(fsize, set())
        freed_block.add(file_locations[fnum])

        file_locations[fnum] = (leftmost_loc[0], leftmost_loc[0] + fsize)
        free_space_blocks[leftmost_size].remove(leftmost_loc)
        new_size = leftmost_size - fsize
        if new_size > 0:
            free_space_blocks[new_size].add(
                (leftmost_loc[0] + fsize, leftmost_loc[0] + fsize + new_size)
            )

    for fnum in sorted(file_locations.keys()):
        start, end = file_locations[fnum]
        checksum += sum([val * fnum for val in range(start, end)])

    return checksum


def print_fs(
    file_locs: dict[int, tuple[int, int]], fs_blocks: dict[int, set[tuple[int, int]]]
):
    fs_str = []
    rev_lookup: dict[tuple[int, int], str] = {
        val: str(key) for key, val in file_locs.items()
    }
    for block_size in fs_blocks:
        for block in fs_blocks[block_size]:
            rev_lookup[block] = "."

    for loc in sorted(rev_lookup.keys()):
        fchar = rev_lookup[loc]
        fs_str += [fchar for i in range(loc[1] - loc[0])]

    return "".join(fs_str)


def main():
    file_map = parse_input()
    print("Part One:")
    print(part_one(file_map))
    print("Part Two:")
    print(part_two(file_map))


if __name__ == "__main__":
    main()
