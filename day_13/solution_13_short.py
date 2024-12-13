import re

def det(a, b):
    return a[0] * b[1] - a[1] * b[0]

def solve(a, b, prize, index):
    result = (det(prize, b) if index == 0 else det(a, prize)) / det(a, b)
    return result if result.is_integer() else 0

print([
    sum(3 * solve(a, b, (prize[0] + offset, prize[1] + offset), 0) + solve(a, b, (prize[0] + offset, prize[1] + offset), 1)
        for d in open('input.txt').read().strip().split('\n\n')
        for a, b, prize in (([int(x) for x in re.findall(r'-?\d+', line)] for line in d.split('\n')),))
    for offset in (0, 1e13)])
