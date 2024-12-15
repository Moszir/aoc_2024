from collections import deque

grid, moves = open('input.txt').read().strip().split('\n\n')
grid = [[c for c in line] for line in grid.split('\n')]
big_grid = [
    [x
     for c in line
     for x in (('#', '#') if c == '#' else ('[', ']') if c == 'O' else ('.', '.') if c == '.' else ('@', '.'))]
    for line in grid]
moves = ''.join(moves.split('\n'))


def solve(g):
    r, c = next((r, c) for r, row in enumerate(g) for c, thing in enumerate(row) if thing == '@')
    g[r][c] = '.'

    for move in moves:
        dr, dc = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}[move]
        new_r, new_c = r + dr, c + dc

        if g[new_r][new_c] == '#':
            continue

        if g[new_r][new_c] == '.':
            r, c = new_r, new_c
            continue

        # We have to push a block
        to_be_processed = deque([(r, c)])
        visited = set()
        pushable = True
        while to_be_processed:
            p = to_be_processed.popleft()
            if p in visited:
                continue
            visited.add(p)

            q = p[0] + dr, p[1] + dc
            gq = g[p[0] + dr][p[1] + dc]
            if gq == '#':
                pushable = False
                break
            to_be_processed.extend(
                [q] if gq == 'O' else
                [q, (q[0], q[1] + 1)] if gq == '[' else
                [q, (q[0], q[1] - 1)] if gq == ']' else
                [])
        if not pushable:
            continue

        # It is pushable, let's push it!
        push = [(p, g[p[0]][p[1]]) for p in visited]
        for p, _ in push:
            g[p[0]][p[1]] = '.'
        for p, q in push:
            g[p[0] + dr][p[1] + dc] = q

        r, c = new_r, new_c

    return sum((100 * r + c) for r, row in enumerate(g) for c, t in enumerate(row) if t in ['[', 'O'])


print(solve(grid))  # 1463512
print(solve(big_grid))  # 1486520
