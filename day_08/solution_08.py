lines = open('input.txt').read().strip().split('\n')
rows = len(lines)
cols = len(lines[0])

things = {}
for r in range(rows):
    for c in range(cols):
        if lines[r][c] != '.':
            if lines[r][c] not in things:
                things[lines[r][c]] = []
            things[lines[r][c]].append((r,c))

antinodes = set()
for r in range(rows):
    for c in range(cols):
        for thing, locations in things.items():
            for (r1, c1) in locations:
                for (r2, c2) in locations:
                    if (r1, c1) != (r2, c2):
                        dist1 = abs(r - r1) + abs(c - c1)
                        dist2 = abs(r - r2) + abs(c - c2)
                        # slope: (r-r1)/(c-c1) == (r-r2)/(c-c2)
                        # except for the case where c-c1 == 0 or c-c2 == 0
                        # but if we multiply both sides by (c-c1)(c-c2) we get
                        # if (dist1 == 2 * dist2 or dist1 * 2 == dist2) and ((r - r1) * (c - c2) == (c - c1) * (r - r2)):
                        if ((r - r1) * (c - c2) == (c - c1) * (r - r2)):
                            antinodes.add((r, c))

print(len(antinodes))
