disk_map = open('input.txt').read().strip()
disk_size = sum(int(c) for c in disk_map)

disk = [None] * disk_size
position = 0
spaces = [[] for i in range(10)]
for i, c in enumerate(disk_map):
    size = int(c)
    if i % 2 == 0:
        # file
        file_id = i // 2
        for i in range(size):
            disk[position] = file_id
            position += 1
    else:
        # space
        spaces[size].append(position)
        position += size

for i, s in enumerate(spaces):
    s.sort(reverse=True)

disk2 = disk.copy()

space_index = next(i for i, value in enumerate(disk) if value is None)
index = disk_size - 1
while index > space_index:
    if disk[index] is None:
        index -= 1
    else:
        file_id = disk[index]
        disk[index] = None
        disk[space_index] = file_id
        space_index += 1
        while disk[space_index] is not None:
            space_index += 1

def checksum(d):
    return sum(i * value for i, value in enumerate(d) if value is not None)

print(checksum(disk))

index = disk_size - 1
last_file_index = disk_size
while index > 0:
    # find the next file
    while index > 0 and (disk2[index] is None or disk2[index] >= last_file_index):
        index -= 1
    file_id = disk2[index]
    last_file_index = file_id
    file_last = index
    while disk2[index] == file_id:
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
        for i in range(file_size):
            disk2[space_index + i] = file_id
            disk2[file_first + i] = None
        spaces[space_size].pop()

        remaining_space_size = space_size - file_size
        if remaining_space_size > 0:
            spaces[remaining_space_size].append(space_index + file_size)
            spaces[remaining_space_size].sort(reverse=True)

print(checksum(disk2))
