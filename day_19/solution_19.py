""" Advent of Code 2024 Day 19 """
from functools import cache

patterns, designs = open("input.txt").read().strip().split('\n\n')
patterns = patterns.split(', ')
designs = designs.split('\n')


@cache
def ways(design):
    if not design:  # Empty string can be formed in one way
        return 1
    return sum(ways(design[len(pattern):]) for pattern in patterns if design.startswith(pattern))


print(sum(1 for design in designs if ways(design) > 0))  # 280
print(sum(ways(design) for design in designs))  # 606411968721181
