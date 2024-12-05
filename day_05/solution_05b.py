from collections import deque

text = open('input.txt').read().strip()
rules, updates = text.split('\n\n')
rules = rules.split('\n')
updates = updates.split('\n')

before = {}
after = {}
for line in rules:
    a, b = map(int, line.split('|'))

    if b not in before:
        before[b] = set()
    before[b].add(a)

    if a not in after:
        after[a] = set()
    after[a].add(b)

# Doing part 1 with the part 2 algorithm:
result1 = 0
result2 = 0
for update in updates:
    ps = [int(p) for p in update.split(',')]

    good = []
    rules_left = {p: len(before[p] & set(ps)) for p in ps}
    q = deque([p for p in ps if rules_left[p] == 0])

    while q:
        x = q.popleft()
        good.append(x)
        for y in after[x]:
            if y in rules_left:
                rules_left[y] -= 1
                if rules_left[y] == 0:
                    q.append(y)

    x = good[len(good) // 2]
    if all((ps[i] == good[i] for i in range(len(ps)))):
        result1 += x
    else:
        result2 += x

print(result1)
print(result2)
