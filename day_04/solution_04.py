lines = open('input.txt').read().strip().split('\n')

g = lines
rr = len(g)
cc = len(g[0])

def xmas(s1, s2, s3, s4):
    return 1 if s1 == 'X' and s2 == 'M' and s3 == 'A' and s4 == 'S' else 0

def mmass(m1, m2, a, s1, s2):
    return 1 if (m1 == 'M' and m2 == 'M' and a == 'A' and s1 == 'S' and s2 == 'S') else 0

x = 0
for r in range(rr):
    for c in range(cc):
        if c+3 < cc:
            x += xmas(g[r][c], g[r][c+1], g[r][c+2], g[r][c+3])
        if r+3 < rr:
            x += xmas(g[r][c], g[r+1][c], g[r+2][c], g[r+3][c])
        if c-3 >= 0:
            x += xmas(g[r][c], g[r][c-1], g[r][c-2], g[r][c-3])
        if r-3 >= 0:
            x += xmas(g[r][c], g[r-1][c], g[r-2][c], g[r-3][c])
        if r+3 < rr and c+3 < cc:
            x += xmas(g[r][c], g[r+1][c+1], g[r+2][c+2], g[r+3][c+3])
        if r-3 >= 0 and c-3 >= 0:
            x += xmas(g[r][c], g[r-1][c-1], g[r-2][c-2], g[r-3][c-3])
        if r+3 < rr and c-3 >= 0:
            x += xmas(g[r][c], g[r+1][c-1], g[r+2][c-2], g[r+3][c-3])
        if r-3 >= 0 and c+3 < cc:
            x += xmas(g[r][c], g[r-1][c+1], g[r-2][c+2], g[r-3][c+3])

print(x)

x = 0
for r in range(rr):
    for c in range(cc):
        if r+2 < rr and c+2 < cc:
            x += mmass(g[r][c], g[r+2][c], g[r+1][c+1], g[r][c+2], g[r+2][c+2])
            x += mmass(g[r][c], g[r][c+2], g[r+1][c+1], g[r+2][c], g[r+2][c+2])
            x += mmass(g[r+2][c+2], g[r][c+2], g[r+1][c+1], g[r+2][c], g[r][c])
            x += mmass(g[r+2][c+2], g[r+2][c], g[r+1][c+1], g[r][c+2], g[r][c])

print(x)
