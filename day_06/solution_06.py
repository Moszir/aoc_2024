grid = open('input.txt').read().strip().split('\n')
rows = len(grid)
cols = len(grid[0])

orig = (-1, -1)

for r in range(rows):
    for c in range(cols):
        if grid[r][c] == '^':
            orig = r, c

assert orig != (-1, -1)

# Start with up, turn right with +1%4
dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

seen = set()
r, c = orig
d = 0
while True:
    seen.add((r, c))
    r2, c2 = r + dirs[d][0], c + dirs[d][1]
    if not 0 <= r2 < rows or not 0 <= c2 < cols:
        break
    if grid[r2][c2] == '#':
        d = (d+1) % 4
        # let it stay in one place, might need more than one turn
    else:
        r, c = r2, c2

print(len(seen))


loops = 0
print(rows * cols)
i = 0
for rb in range(rows):
    for cb in range(cols):
        i += 1
        if (i % 100 == 0):
            print(f'{i=}')
        seen = set()
        r, c = orig
        d = 0
        while True:
            if (r, c, d) in seen:
                loops += 1
                break
            seen.add((r, c, d))
            r2, c2 = r + dirs[d][0], c + dirs[d][1]
            if not 0 <= r2 < rows or not 0 <= c2 < cols:
                break
            if grid[r2][c2] == '#' or (r2 == rb and c2 == cb):
                d = (d+1) % 4
                # let it stay in one place, might need more than one turn
            else:
                r, c = r2, c2

print(loops)