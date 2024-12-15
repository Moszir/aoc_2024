import copy
from collections import deque

grid, moves = open('input.txt').read().strip().split('\n\n')
moves = ''.join(moves.split('\n'))

replace_with = {
    '#': ('#', '#'),
    'O': ('[', ']'),
    '.': ('.', '.'),
    '@': ('@', '.')
}
grid = [[x for c in line for x in replace_with[c]] for line in grid.split('\n')]
original_robot = next((r, c) for r, row in enumerate(grid) for c, thing in enumerate(row) if thing == '@')
grid[original_robot[0]][original_robot[1]] = '.'


def solve(horizontal_step_factor=1):
    g = copy.deepcopy(grid)
    r, c = original_robot

    for move in moves:
        dr, dc = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}[move]
        new_r, new_c = r + dr, c + dc * horizontal_step_factor

        if g[new_r][new_c] == '#':
            continue

        if g[new_r][new_c] == '.':
            r, c = new_r, new_c
            continue

        to_be_processed = deque([(r, c + j) for j in range(horizontal_step_factor)])
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
                [q, (q[0], q[1] + 1)] if gq == '[' else
                [q, (q[0], q[1] - 1)] if gq == ']' else
                [])
        if not pushable:
            continue

        push = [(p, g[p[0]][p[1]]) for p in visited]
        for p, _ in push:
            g[p[0]][p[1]] = '.'
        for p, q in push:
            g[p[0] + dr][p[1] + dc * horizontal_step_factor] = q

        r, c = new_r, new_c

    return sum((100 * r + c // horizontal_step_factor) for r, row in enumerate(g) for c, t in enumerate(row) if t == '[')


print(solve(2))
print(solve())
