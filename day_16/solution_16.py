""" Advent of Code 2024 Day 16

https://adventofcode.com/2024/day/16
"""
import heapq

grid = open('input.txt').read().strip().split('\n')
# The border of the grid is all walls, so we can skip the range checking

rows = len(grid)
cols = len(grid[0])
starting_position = (139, 1, 0, 1)  # (row, col, d_row, d_col)
target_positions = [(1, 139, 0, 1), (1, 139, -1, 0)]


def possible_moves_and_scores(r, c, dr, dc):
    result = [
        (1000, (r, c, -dc, dr)),  # turn left
        (1000, (r, c, dc, -dr)),  # turn right
    ]
    if grid[r + dr][c + dc] != '#':
        result.append((1, (r + dr, c + dc, dr, dc)))  # move forward
    return result


best_scores = {starting_position: 0}
to_be_processed = []
heapq.heappush(to_be_processed, (0, starting_position))

while to_be_processed:
    score, position = heapq.heappop(to_be_processed)
    for move_score, new_position in possible_moves_and_scores(*position):
        new_score = score + move_score
        if new_position not in best_scores or new_score < best_scores[new_position]:
            best_scores[new_position] = new_score
            heapq.heappush(to_be_processed, (new_score, new_position))

for target_position in target_positions:
    if target_position in best_scores:
        print(best_scores[target_position])

best_spots = {(1, 139)}
to_be_processed = [(1, 139, 83444)]
while to_be_processed:
    r, c, score = to_be_processed.pop()
    for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        new_r, new_c = r - dr, c - dc
        if grid[new_r][new_c] != '#' and (new_r, new_c, dr, dc) in best_scores:
            if best_scores[(new_r, new_c, dr, dc)] < score:
                best_spots.add((new_r, new_c))
                to_be_processed.append((new_r, new_c, best_scores[(new_r, new_c, dr, dc)]))

print(len(best_spots))
