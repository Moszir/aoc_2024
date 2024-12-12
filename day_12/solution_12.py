lines = open('input.txt').read().strip().split('\n')
rows = len(lines)
cols = len(lines[0])

processed = [[False] * cols for _ in range(rows)]

cost1 = 0
cost2 = 0
for r in range(rows):
    for c in range(cols):
        if processed[r][c]:
            continue

        # We found a new group
        character = lines[r][c]
        area = 0
        perimeter = 0
        to_be_processed = {(r, c)}
        perimeters = {
            (dr, dc): []
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0))
        }

        while to_be_processed:
            rr, cc = to_be_processed.pop()
            processed[rr][cc] = True
            area += 1

            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_r, new_c = rr + dr, cc + dc
                if not 0 <= new_r < rows or not 0 <= new_c < cols:
                    perimeter += 1  # outer border
                    perimeters[(dr, dc)].append((rr, cc))
                else:
                    if lines[new_r][new_c] != character:
                        perimeter += 1  # border with different character
                        perimeters[(dr, dc)].append((rr, cc))
                    elif not processed[new_r][new_c]:
                        to_be_processed.add((new_r, new_c))
                    else:
                        # neighbor is the same character (-> no border), but already processed
                        pass

        sides = 0
        for (dr, dc), points in perimeters.items():
            prd = [False] * len(points)
            for i, (r1, c1) in enumerate(points):
                if not prd[i]:
                    prd[i] = True
                    sides += 1
                    dir1 = (-dc, dr)
                    r2, c2 = r1, c1
                    while True:
                        r2 += dir1[0]
                        c2 += dir1[1]
                        if (r2, c2) in points:
                            prd[points.index((r2, c2))] = True
                        else:
                            break
                    r2, c2 = r1, c1
                    dir2 = (dc, -dr)
                    while True:
                        r2 += dir2[0]
                        c2 += dir2[1]
                        if (r2, c2) in points:
                            prd[points.index((r2, c2))] = True
                        else:
                            break

        cost1 += area * perimeter
        cost2 += area * sides

print(cost1)
print(cost2)
