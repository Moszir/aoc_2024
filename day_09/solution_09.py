disk_map = open('input.txt').read().strip()
disk_size = sum(int(c) for c in disk_map)
print(disk_size)

disk = [None] * disk_size
position = 0
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
        position += size

part2_disk = disk.copy()

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

print(sum(i * value for i, value in enumerate(disk) if value is not None))

print(part2_disk[:25])
index = disk_size - 1
last_file_index = disk_size
while index > 0:
    # find the next file
    while index > 0 and (part2_disk[index] is None or part2_disk[index] >= last_file_index):
        index -= 1
    print(index)
    file_id = part2_disk[index]
    last_file_index = file_id
    file_last = index
    while part2_disk[index] == file_id:
        index -= 1
    file_first = index + 1
    file_size = file_last - file_first + 1

    # find the first space that can fit the file
    space_index = next((i for i in range(disk_size) if all((part2_disk[i + j] is None for j in range(file_size)))), None)
    if space_index is not None and space_index < file_first:
        # move the file to the space
        for i in range(file_size):
            part2_disk[space_index + i] = file_id
            part2_disk[file_first + i] = None

print(part2_disk[:25])
print(sum(i * value for i, value in enumerate(part2_disk) if value is not None))
