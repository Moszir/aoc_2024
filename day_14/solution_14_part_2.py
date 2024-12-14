""" Advent of Code day 14

https://adventofcode.com/2024/day/14
"""
import dataclasses
import re
import typing

x_max = 101
x_half = 50
y_max = 103
y_half = 51


@dataclasses.dataclass
class Position:
    """ Represents a position on the grid """
    x: int
    y: int

    def __add__(self, other) -> 'Position':
        return Position(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def neighbors(self):
        """ Generates the neighbors of the position that are within the bounds """
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < x_max and 0 <= ny < y_max:
                yield Position(nx, ny)


@dataclasses.dataclass
class Guard:
    """ Represents a guard """
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


class GuardMap:
    """ Represents the guard map """

    def __init__(self, _guards: typing.List[Guard]):
        self.guard_map = [
            ['.' for _ in range(x_max)]
            for _ in range(y_max)]
        for _guard in _guards:
            self.guard_map[_guard.position.y][_guard.position.x] = '#'

    def occupied(self, position: Position) -> bool:
        """ Return True if the position is occupied """
        return self.guard_map[position.y][position.x] == '#'

    @staticmethod
    def positions():
        """ Generate all positions """
        for y in range(y_max):
            for x in range(x_max):
                yield Position(x, y)

    def components(self) -> int:
        """ Return the number of components """
        visited = set()
        components = 0
        for p in self.positions():
            if self.occupied(p) and p not in visited:
                components += 1
                to_be_processed = [p]
                while to_be_processed:
                    q = to_be_processed.pop()
                    visited.add(q)
                    for n in q.neighbors():
                        if self.occupied(n) and n not in visited:
                            to_be_processed.append(n)
        return components

    def print(self) -> None:
        """ Print the guard map """
        for y in range(y_max):
            print(''.join(self.guard_map[y]))


guards = [
    Guard(Position(x, y), Position(vx, vy))
    for d in open('input.txt').read().strip().split('\n')
    for x, y, vx, vy in [map(int, re.findall(r'-?\d+', d))]
]

move_counter = 0
while True:
    guard_map = GuardMap(guards)
    if guard_map.components() < 200:
        print(f'Solution: {move_counter}')
        print(f'There are {guard_map.components()} components:')
        guard_map.print()
        break

    for guard in guards:
        guard.move()
    move_counter += 1

# 7687
