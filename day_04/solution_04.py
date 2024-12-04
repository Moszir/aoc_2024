lines = open('input.txt').read().strip().split('\n')

g = lines
rr = len(g)
cc = len(g[0])

def xmas(s1, s2, s3, s4):
    s = s1 + s2 + s3 + s4
    return 1 if s == 'XMAS' or s == 'SAMX' else 0

x = 0
for r in range(rr):
    for c in range(cc):
        if c+3 < cc:
            x += xmas(g[r][c], g[r][c+1], g[r][c+2], g[r][c+3])
        if r+3 < rr:
            x += xmas(g[r][c], g[r+1][c], g[r+2][c], g[r+3][c])
        if r+3 < rr and c+3 < cc:
            x += xmas(g[r][c], g[r+1][c+1], g[r+2][c+2], g[r+3][c+3])
        if r+3 < rr and c-3 >= 0:
            x += xmas(g[r][c], g[r+1][c-1], g[r+2][c-2], g[r+3][c-3])

print(x)

x = 0
for r in range(rr-2):
    for c in range(cc-2):
        if g[r+1][c+1] == 'A':
            corners = g[r][c] + g[r][c+2] + g[r+2][c+2] + g[r+2][c]
            if corners in ('MMSS', 'MSSM', 'SSMM', 'SMMS'):
                x += 1

print(x)
