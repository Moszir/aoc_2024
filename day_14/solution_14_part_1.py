""" Advent of Code day 14

https://adventofcode.com/2024/day/14
"""
import dataclasses
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
        return Position(self.x + other.x, self.y + other.y)


@dataclasses.dataclass
class Guard:
    position: Position
    velocity: Position

    def __repr__(self):
        return f'{self.position=}, {self.velocity=}'

    def move(self) -> None:
        """ Move the guard """
        self.position += self.velocity
        self.position.x %= x_max
        self.position.y %= y_max

    def quadrant(self) -> int:
        """ Return the quadrant the guard is in """
        if self.position.x < x_half and self.position.y < y_half:
            return 0
        elif self.position.x > x_half and self.position.y < y_half:
            return 1
        elif self.position.x < x_half and self.position.y > y_half:
            return 2
        elif self.position.x > x_half and self.position.y > y_half:
            return 3
        return 4


guards = [
    Guard(Position(x, y), Position(vx, vy))
    for d in open('input.txt').read().strip().split('\n')
    for x, y, vx, vy in [map(int, re.findall(r'-?\d+', d))]
]

quadrant_scores = [0, 0, 0, 0, 0]  # 4 quadrants and a middle
for guard in guards:
    for _ in range(100):
        guard.move()
    quadrant_scores[guard.quadrant()] += 1

print(quadrant_scores[0] * quadrant_scores[1] * quadrant_scores[2] * quadrant_scores[3])
# 214109808
