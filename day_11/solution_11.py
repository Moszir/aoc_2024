from functools import cache

numbers = list(map(int, open('input.txt').read().strip().split()))

@cache
def count(stone, steps):
    if steps == 0:
        return 1
    if stone == 0:
        return count(1, steps - 1)
    if len(str(stone)) % 2 == 0:
        s = str(stone)
        left, right = int(s[:len(s) // 2]), int(s[len(s) // 2:])
        return count(left, steps - 1) + count(right, steps - 1)
    return count(2024 * stone, steps - 1)

for step in (25, 75):
    print(sum(count(stone, step) for stone in numbers))
