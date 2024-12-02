lines = open('input.txt').read().strip().split('\n')
left = []
right = []
counter = {}

for line in lines:
    l, r = line.split()
    r = int(r)
    left.append(int(l))
    right.append(r)
    if r in counter:
        counter[r] += 1
    else:
        counter[r] = 1

print(sum(abs(r-l) for l, r in zip(sorted(left), sorted(right))))
print(sum(l * counter.get(l, 0) for l in left))
