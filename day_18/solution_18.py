""" Advent of Code 2024 Day 18
"""
from collections import deque
import typing

lines = open('input.txt').read().strip().split('\n')

N = 71
G = [['.' for _ in range(N)] for _ in range(N)]
start = (0, 0)
target = (70, 70)


def path() -> typing.Optional[int]:
    global G
    visited = set()
    to_be_processed = deque([(0, start)])
    while to_be_processed:
        d, p = to_be_processed.popleft()
        if p == target:
            return d
        if p in visited:
            continue
        visited.add(p)
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            q = (p[0] + dr, p[1] + dc)
            if 0 <= q[0] < N and 0 <= q[1] < N and G[q[0]][q[1]] != '#':
                to_be_processed.append((d + 1, q))
    return None


for line in lines[:1024]:
    x, y = map(int, line.split(','))
    G[y][x] = '#'
print(path())

for i, line in enumerate(lines[1024:], 1024):
    x, y = map(int, line.split(','))
    G[y][x] = '#'
    if path() is None:
        print(f'{x},{y}')  # 58,19
        break
