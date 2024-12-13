import re

def det(a, b):
    return a[0] * b[1] - a[1] * b[0]

def solve(a, b, prize):
    result = (det(prize, b) / det(a, b), det(a, prize) / det(a, b))
    return result if all((x.is_integer() and x >= 0 for x in result)) else (0, 0)

print([
    sum(sum([3, 1][i] * solve(a, b, (prize[0] + offset, prize[1] + offset))[i] for i in (0, 1))
        for d in open('input.txt').read().strip().split('\n\n')
        for a, b, prize in (([int(x) for x in re.findall(r'-?\d+', line)] for line in d.split('\n')),))
    for offset in (0, 1e13)])
