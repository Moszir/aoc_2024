""" Advent of Code 2024 Day 22
BAAAAAA!!!

- Júlia
"""
from collections import defaultdict

numbers = [b for b in map(int, open('input.txt').read().strip().split('\n'))]


def evolve(number: int, times: int = 1) -> int:
    for _ in range(times):
        number = ((64 * number) ^ number) % 2 ** 24
        number = ((number // 32) ^ number) % 2 ** 24
        number = ((number * 2_048) ^ number) % 2 ** 24
    return number


print(sum(evolve(number, 2000) for number in numbers))  # 15608699004

sequences = defaultdict(int)

for number in numbers:
    buyer = [number % 10]
    for _ in range(2000):
        number = evolve(number)
        buyer.append(number % 10)

    seen = set()
    for i in range(len(buyer) - 4):
        sequence = tuple((x - y for x, y in zip(buyer[i + 1:i + 5], buyer[i:i + 4])))
        if sequence not in seen:
            seen.add(sequence)
            sequences[sequence] += buyer[i + 4]

print(max(sequences.values()))  # 1791
