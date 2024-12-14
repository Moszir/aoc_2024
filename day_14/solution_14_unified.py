""" Advent of Code day 14

https://adventofcode.com/2024/day/14

OBVIOUSLY, the Christmas tree Easter egg will minimize the safety score of the grid.
I mean, it's a Christmas tree, it's supposed to be safe, right?
What else would the connection be between part 1 and part 2?
"""
import dataclasses
import math
import re

x_max = 101
x_half = 50
y_max = 103
y_half = 51


@dataclasses.dataclass
class Position:
    x: int
    y: int

    def __add__(self, other) -> 'Position':
        return Position((self.x + other.x) % x_max, (self.y + other.y) % y_max)


@dataclasses.dataclass
class Guard:
    position: Position
    velocity: Position

    def move(self) -> None:
        """ Move the guard """
        self.position += self.velocity

    def quadrant(self) -> int:
        """ Return the quadrant the guard is in """
        return (
            4 if self.position.x == x_half or self.position.y == y_half else
            (0 if self.position.x < x_half else 1) + (0 if self.position.y < y_half else 2))


guards = [
    Guard(Position(x, y), Position(vx, vy))
    for d in open('input.txt').read().strip().split('\n')
    for x, y, vx, vy in [map(int, re.findall(r'-?\d+', d))]
]

best_round = -1
best_safety_score = 125 ** 4 + 1  # The highest possible score is when all 4 quadrants have 125 guards

for move in range(math.lcm(x_max, y_max)):
    quadrants = [0, 0, 0, 0, 0]  # 4 quadrants and a middle
    for guard in guards:
        quadrants[guard.quadrant()] += 1
        guard.move()
    safety_score = math.prod(quadrants[:4])
    if safety_score < best_safety_score:
        best_safety_score = safety_score
        best_round = move
    if move == 100:
        print(f'Part 1 solution: {safety_score}')
        # 214_109_808

print(f'Part 2 solution: {best_round}')
# 7_687
