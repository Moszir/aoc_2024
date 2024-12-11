from collections import defaultdict


numbers = list(map(int, open('input.txt').read().strip().split()))
counts = defaultdict(int)
for n in numbers:
    counts[n] += 1

for c in range(75):
    next_counts = defaultdict(int)
    for n, count in counts.items():
        if n == 0:
            next_counts[1] += count
            continue
        s = str(n)
        if len(s) % 2 == 0:
            left, right = int(s[:len(s) // 2]), int(s[len(s) // 2:])
            next_counts[left] += count
            next_counts[right] += count
        else:
            next_counts[2024 * n] += count
    counts = next_counts

print(sum(counts.values()))
