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


# Part 1
result = 0
for update in updates:
    ps = [int(p) for p in update.split(',')]

    if all((ps[i] not in after[ps[j]]
            for i in range(len(ps))
            for j in range(i+1, len(ps)))):
        result += ps[len(ps) // 2]

print(result)


# Part 2
result = 0
for update in updates:
    ps = [int(p) for p in update.split(',')]

    ok = all((
        ps[i] not in after[ps[j]]
        for i in range(len(ps))
        for j in range(i+1, len(ps))
    ))

    if not ok:
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
        result += good[len(good) // 2]

print(result)
