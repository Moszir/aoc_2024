import typing

g = open('input.txt').read().strip().split('\n')
assert(all(len(row) == len(g[0]) for row in g))  # rectangular

Direction = typing.Tuple[int, int]
Directions = typing.List[Direction]

def count(text: str, directions: Directions) -> int:
    assert(len(text) == len(directions) + 1)
    global g

    result = 0
    for r in range(len(g)):
        for c in range(len(g[0])):
            if g[r][c] == text[0]:
                match = True
                r2, c2 = r, c
                for i in range(len(directions)):
                    d = directions[i]
                    r2 += d[0]
                    c2 += d[1]
                    if r2 < 0 or r2 >= len(g) or c2 < 0 or c2 >= len(g[r2]) or g[r2][c2] != text[i+1]:
                        match = False
                        break
                if match:
                    result += 1
    return result

print(
    sum(count('XMAS', [d]*3)
        for d in (
            (dr, dc)
            for dr in (-1, 0, 1)
            for dc in (-1, 0, 1)
        )))  # The (0,0) direction will obviously not give any result.

# Start from the 'A', and go around the corners
X = [(-1, -1), (0, 2), (2, 0), (0, -2)]
print(
    sum(
        count(text, X)
        for text in ('AMMSS', 'ASMMS', 'ASSMM', 'AMSSM')))
