""" Advent of Code 2024 Day 16

https://adventofcode.com/2024/day/16
"""
import networkx as nx

grid = open('input.txt').read().strip().split('\n')

starting_position = None
target_positions = None
G = nx.DiGraph()
for r, row in enumerate(grid):
    for c, cell in enumerate(row):
        if cell != '#':
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                G.add_edge((r, c, dr, dc), (r, c, -dc, dr), weight=1000)  # turns
                G.add_edge((r, c, dr, dc), (r, c, dc, -dr), weight=1000)
                if grid[r + dr][c + dc] != '#':
                    G.add_edge((r, c, dr, dc), (r + dr, c + dc, dr, dc), weight=1)  # forward

            if cell == 'S':
                starting_position = (r, c, 0, 1)  # problem statement says we start facing east
            if cell == 'E':
                assert target_positions is None
                target_positions = [(r, c, 1, 0), (r, c, -1, 0), (r, c, 0, 1), (r, c, 0, -1)]

assert starting_position is not None
assert target_positions is not None

costs = {tp: nx.shortest_path_length(G, source=starting_position, target=tp, weight='weight') for tp in target_positions}
min_cost = min(costs.values())
print(min_cost)
print(len(set((r, c)
              for tp, cost in costs.items() if cost == min_cost
              for sp in nx.all_shortest_paths(G, source=starting_position, target=tp, weight='weight')
              for r, c, _, _ in sp)))
