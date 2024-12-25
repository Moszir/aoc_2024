locks = []
keys = []

for grid in [x.split('\n') for x in open('input.txt').read().strip().split('\n\n')]:
    pattern = [sum(1 for r in range(len(grid)) if grid[r][c] == "#") - 1 for c in range(len(grid[0]))]
    if grid[0][0] == "#":
        locks.append(pattern)
    else:
        keys.append(pattern)

print(sum(1 for lock in locks for key in keys if all(x + y <= 5 for x, y in zip(lock, key))))  # 3107
