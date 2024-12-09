disk_map = open('input.txt').read().strip()
disk_size = sum(int(c) for c in disk_map)
disk = [None] * disk_size
spaces = [[] for i in range(10)]

position = 0
for i, c in enumerate(disk_map):
    size = int(c)
    if i % 2 == 0:  # file
        file_id = i // 2
        for i in range(size):
            disk[position] = file_id
            position += 1
    elif size > 0:  # space > 0
        spaces[size].append(position)
        position += size

for i, s in enumerate(spaces):
    s.sort(reverse=True)

accu = 0
space_index = next(i for i, value in enumerate(disk) if value is None)
for index in range(disk_size-1, -1, -1):
    if disk[index] is not None:
        if index > space_index:
            accu += space_index * disk[index]
            space_index += 1
            while disk[space_index] is not None:
                space_index += 1
        else:
            accu += index * disk[index]

print(accu)

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

print(accu)
