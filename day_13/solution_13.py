# Solve the following system of equations:
# a.x * u + b.x * v == prize.x
# a.y * u + b.y * v == prize.y
#
# We can rewrite this as:
# u = (prize.x - b.x * v) / a.x
# a.y * ((prize.x - b.x * v) / a.x) + b.y * v == prize.y
# a.y * (prize.x - b.x * v) + b.y * v * a.x == prize.y * a.x
# a.y * prize.x - a.y * b.x * v + b.y * v * a.x == prize.y * a.x
# (a.x * b.y - a.y * b.x) * v == prize.y * a.x - a.y * prize.x
def solve(a, b, prize):
    assert a[0] != 0
    c = a[0] * b[1] - a[1] * b[0]
    if c != 0:
        v = (prize[1] * a[0] - a[1] * prize[0]) / c
        u = (prize[0] - b[0] * v) / a[0]
        if u.is_integer() and v.is_integer():
            return int(u), int(v)
    return None


part1 = 0
part2 = 0
for d in open('input.txt').read().strip().split('\n\n'):
    lines = d.split('\n')
    assert len(lines) == 3

    a, b, prize = ((line.split(',') for line in lines))
    a = (int(a[0].split('+')[1]), int(a[1].split('+')[1]))
    b = (int(b[0].split('+')[1]), int(b[1].split('+')[1]))
    prize = (int(prize[0].split('=')[1]), int(prize[1].split('=')[1]))

    x = solve(a, b, prize)
    if x is not None:
        part1 += 3 * x[0] + x[1]
    x = solve(a, b, (prize[0] + 10_000_000_000_000, prize[1] + 10_000_000_000_000))
    if x is not None:
        part2 += 3 * x[0] + x[1]

print(part1)
print(part2)
