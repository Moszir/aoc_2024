""" Advent of Code 2024 Day 20 """
from collections import deque

grid = open('input.txt').read().strip().split('\n')
rows = len(grid)
cols = len(grid[0])

start = next((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 'S')
end = next((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 'E')

distance_to_end = {}
to_be_processed = deque([(0, end[0], end[1])])
while to_be_processed:
    d, r, c = to_be_processed.popleft()
    if (r, c) in distance_to_end:
        continue
    distance_to_end[(r, c)] = d
    for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        rr, cc = r + dr, c + dc
        if 0 <= rr < rows and 0 <= cc < cols and grid[rr][cc] != '#':
            to_be_processed.append((d + 1, rr, cc))


def find_cheat(allowed_cheat_time):
    # distance already covered, start of cheat, time left for cheat, r, c
    to_be_processed = deque([(0, None, None, start[0], start[1])])

    # position, start of cheat, time left for cheat
    cheat_visited = set()

    # Cheats that start and end at the same place are considered the same cheat, regardless of the path.
    cheats = set()

    while to_be_processed:
        distance, cheat_start, cheat_time_remaining, r, c = to_be_processed.popleft()

        # This won't be a good enough cheat
        if distance >= distance_to_end[start] - 100:
            continue

        if (r, c, cheat_start, cheat_time_remaining) in cheat_visited:
            continue
        cheat_visited.add((r, c, cheat_start, cheat_time_remaining))

        # We can possibly start a cheat here
        if cheat_start is None and grid[r][c] != '#':
            to_be_processed.append((distance, (r, c), allowed_cheat_time, r, c))

        # We can possibly end a cheat here
        if cheat_time_remaining is not None and grid[r][c] != '#':  # end cheat
            if distance + distance_to_end[(r, c)] + 100 <= distance_to_end[start]:
                cheats.add((cheat_start, (r, c)))

        # We can move
        if cheat_time_remaining is None or cheat_time_remaining > 0:
            for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                rr, cc = r + dr, c + dc
                # still cheating...
                if cheat_time_remaining is not None:
                    if 0 <= rr < rows and 0 <= cc < cols:
                        to_be_processed.append((distance + 1, cheat_start, cheat_time_remaining - 1, rr, cc))
                else:
                    # Not yet started cheating
                    if 0 <= rr < rows and 0 <= cc < cols and grid[rr][cc] != '#':
                        to_be_processed.append((distance + 1, cheat_start, cheat_time_remaining, rr, cc))

    return len(cheats)


print(find_cheat(2))  # 1378
print(find_cheat(20))  # 975_379
