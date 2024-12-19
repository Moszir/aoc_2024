""" Advent of Code 2024 Day 19 """
from functools import cache


patterns, designs = open("input.txt").read().strip().split('\n\n')
patterns = patterns.split(', ')
designs = designs.split('\n')


@cache
def ways(design):
    if not design:  # Empty string can be formed in one way
        return 1
    global patterns
    result = 0
    for pattern in patterns:
        if design.startswith(pattern):
            result += ways(design[len(pattern):])
    return result


part1 = 0
part2 = 0
for design in designs:
    target_ways = ways(design)
    if target_ways > 0:
        part1 += 1
    part2 += target_ways

print(part1)  # 280
print(part2)  # 606411968721181
