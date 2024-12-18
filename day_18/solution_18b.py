""" Advent of Code 2024 Day 18
"""
import copy
from collections import deque
import typing

lines = open('input.txt').read().strip().split('\n')

N = 71
G = ([[-1 for _ in range(N + 2)]]
     + [[-1] + [5000 for _ in range(N)] + [-1] for _ in range(N)]
     + [[-1 for _ in range(N + 2)]])
start = (1, 1)
target = (71, 71)


def path(last_stone: int) -> typing.Optional[int]:
    global G
    g = copy.deepcopy(G)
    to_be_processed = deque([(0, start)])
    while to_be_processed:
        d, p = to_be_processed.popleft()
        if p == target:
            return d
        if g[p[0]][p[1]] <= last_stone:
            continue
        g[p[0]][p[1]] = -1
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            q = (p[0] + dr, p[1] + dc)
            if g[q[0]][q[1]] > last_stone:
                to_be_processed.append((d + 1, q))
    return None


for i, line in enumerate(lines):
    x, y = map(int, line.split(','))
    G[y + 1][x + 1] = i  # It becomes a stone at round i

print(path(1023))

ok = 1023
assert path(len(lines)) is None
not_ok = len(lines)
while not_ok > ok + 1:
    mid = (ok + not_ok) // 2
    if path(mid) is None:
        not_ok = mid
    else:
        ok = mid
print(lines[not_ok])
