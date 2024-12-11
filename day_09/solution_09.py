import typing


disk_map = open('input.txt').read().strip()
disk_size = sum(int(c) for c in disk_map)

# This list will represent the disk, where each element is the file id of the file at that position,
# or None if there is no file at that position.
disk: typing.List[typing.Optional[int]] = [None] * disk_size

# This list will represent the spaces in the disk at the beginning.
# `spaces[i]` will be a list of the indexes of the spaces of size `i`.
spaces = [[] for _ in range(10)]

position = 0
for i, c in enumerate(disk_map):
    size = int(c)
    if i % 2 == 0:  # file
        file_id = i // 2
        for _ in range(size):
            disk[position] = file_id
            position += 1
    elif size > 0:  # space > 0
        # We skip 0, since we cannot do anything with it.
        spaces[size].append(position)
        position += size

# We will want to use the space with the lowest index first, so we sort the spaces in descending order,
# as popping the last element of the list is easier than popping the first element.
for i, s in enumerate(spaces):
    s.sort(reverse=True)

########################################################################################################################
# Part 1
#
# We will iterate over the disk from the end to the beginning.
# We will keep track of the index of the first space in the disk.
# Instead of moving the files to the spaces, we will calculate the checksum directly.
# This saves some time, and we won't have to restore the disk to its original state for part 2.
accu = 0
space_index = next(i for i, value in enumerate(disk) if value is None)
for index in range(disk_size-1, -1, -1):
    if disk[index] is not None:
        if index > space_index:
            # move the file to the space
            accu += space_index * disk[index]
            # find the next space
            space_index += 1
            while disk[space_index] is not None:
                space_index += 1
        else:
            # file stays in place
            accu += index * disk[index]

# 6288707484810
print(accu)


########################################################################################################################
# Part 2
#
# We will iterate over the disk from the end to the beginning.
# For each file, we will find the first space that can fit the file.
# We will calculate the checksum for the moved file.
# We will update the list of spaces accordingly.
#   For example, if we move a file of size 3 to a space of size 5,
#   then we will remove the space of size 5 and add a space of size 2 to `spaces[2]`, and sort it.
accu = 0
index = disk_size - 1
last_file_index = disk_size
while index > 0:
    # find the next file
    while index > 0 and (disk[index] is None or disk[index] >= last_file_index):
        index -= 1
    file_id = disk[index]
    last_file_index = file_id
    file_last = index
    while disk[index] == file_id:
        index -= 1
    file_first = index + 1
    file_size = file_last - file_first + 1

    # find the first space that can fit the file
    space_size = None
    space_index = disk_size
    for s in range(file_size, 10):
        if spaces[s] and spaces[s][-1] < space_index:
            space_size = s
            space_index = spaces[s][-1]

    if space_index < file_first:
        # move the file to the space
        accu += sum(i * file_id for i in range(space_index, space_index + file_size))

        spaces[space_size].pop()
        remaining_space_size = space_size - file_size
        if remaining_space_size > 0:
            spaces[remaining_space_size].append(space_index + file_size)
            spaces[remaining_space_size].sort(reverse=True)
    else:
        # file stays in place
        accu += sum(i * file_id for i in range(file_first, file_last + 1))

# 6311837662089
print(accu)
