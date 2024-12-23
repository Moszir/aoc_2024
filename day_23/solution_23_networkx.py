""" 2024 Advent of Code Day 23 """
import networkx as nx

G = nx.Graph()
for line in open('input.txt').read().strip().split('\n'):
    v, w = line.split('-')
    G.add_edge(v, w)

# Find the number of triangles that contain at least one node starting with 't'
print(sum(1 for c in nx.enumerate_all_cliques(G) if len(c) == 3 and any(n.startswith('t') for n in c)))  # 1348
# Find the largest clique in the graph and print its nodes sorted alphabetically
print(','.join(sorted(max(nx.enumerate_all_cliques(G), key=len))))  # am,bv,ea,gh,is,iy,ml,nj,nl,no,om,tj,yv
