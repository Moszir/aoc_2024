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

def jump(r, c, dir, block):
    while True:
        rr = r + dir[0]
        cc = c + dir[1]
        if not (0 <= rr < rows and 0 <= cc < cols):
            return None
        if grid[rr][cc] == '#' or (rr == block[0] and cc == block[1]):
            return r, c
        r, c = rr, cc

# Takes around 2s on my PC
loops = 0
for rb, cb in seen:
    seen_corner = set()  # only the up -> right (0 -> 1)
    pos = orig
    d = 0
    while True:
        pos = jump(pos[0], pos[1], dirs[d], (rb, cb))
        if pos is None:
            break
        if d == 0:
            if pos in seen_corner:
                loops += 1
                break
            seen_corner.add(pos)
        d = (d+1)%4

print(loops)
