""" 2024 Advent of Code Day 23

Part 2 solution with the Bron-Kerbosch algorithm.
"""
from collections import defaultdict

nodes = set()
edges = defaultdict(list)
for line in open('input.txt').read().strip().split('\n'):
    v, w = line.split('-')
    nodes.add(v)
    nodes.add(w)
    edges[v].append(w)
    edges[w].append(v)

# Part 1
# Find the number of triangles that contain at least one node starting with 't'
# This is pretty slow (~10 seconds), but it's a Python one-liner.
#
# from itertools import combinations
# print(sum(1 for c in combinations(nodes, 3) if all(a in edges[b] for a, b in combinations(c, 2)) and any(n.startswith('t') for n in c)))  # 1348

# Part 2
def bron_kerbosch(r, p, x):
    """ Bron-Kerbosch algorithm for finding maximal cliques in a graph

    https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
    """
    if not p and not x:
        yield r
    for v in list(p):
        yield from bron_kerbosch(r | {v}, p & set(edges[v]), x & set(edges[v]))
        p.remove(v)
        x.add(v)

maximal_cliques = list(bron_kerbosch(set(), nodes, set()))
print(','.join(sorted(max(maximal_cliques, key=len))))  # am,bv,ea,gh,is,iy,ml,nj,nl,no,om,tj,yv
