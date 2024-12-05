import functools

rules, updates = open('input.txt').read().strip().split('\n\n')
edges = set(tuple(map(int, rule.split('|'))) for rule in rules.split('\n'))

part1 = 0
part2 = 0
for update in updates.split('\n'):
    x = [int(n) for n in update.split(',')]
    y = sorted(x, key=functools.cmp_to_key(lambda u, v: 1 if (v, u) in edges else -1 if (u, v) in edges else 0))
    n = len(x)
    if all((x[i] == y[i] for i in range(n))):
        part1 += x[len(x) // 2]
    else:
        part2 += y[len(y) // 2]

print(part1)
print(part2)
