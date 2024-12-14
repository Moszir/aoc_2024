""" Advent of Code day 14

https://adventofcode.com/2024/day/14
"""
import dataclasses
import math
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


class RecordKeeper:
    def __init__(self, minimize=False):
        self.maximize = not minimize
        self.record = -1 if self.maximize else 100_000

    def update(self, value) -> bool:
        if self.maximize and value > self.record:
            self.record = value
            return True
        if not self.maximize and value < self.record:
            self.record = value
            return True
        return False


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

    def number_of_components(self) -> int:
        """ Returns the number of components """
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

    def largest_component(self) -> int:
        """ Returns the size of the largest component """
        visited = set()
        largest_component_size = RecordKeeper()
        for p in self.positions():
            if self.occupied(p) and p not in visited:
                this_component = set()
                to_be_processed = [p]
                while to_be_processed:
                    q = to_be_processed.pop()
                    this_component.add(q)
                    visited.add(q)
                    for n in q.neighbors():
                        if self.occupied(n) and n not in visited:
                            to_be_processed.append(n)
                largest_component_size.update(len(this_component))
        return largest_component_size.record

    def most_occupied_in_a_row_consecutively(self) -> int:
        """ Returns the most consecutively occupied cells in a row """
        most_occupied = RecordKeeper()
        for y in range(y_max):
            occupied = 0
            for x in range(x_max):
                if self.guard_map[y][x] == '#':
                    occupied += 1
                else:
                    most_occupied.update(occupied)
                    occupied = 0
            most_occupied.update(occupied)
        return most_occupied.record

    def most_occupied_in_a_column_consecutively(self) -> int:
        """ Returns the most consecutively occupied cells in a column """
        most_occupied = RecordKeeper()
        for x in range(x_max):
            occupied = 0
            for y in range(y_max):
                if self.guard_map[y][x] == '#':
                    occupied += 1
                else:
                    most_occupied.update(occupied)
                    occupied = 0
            most_occupied.update(occupied)
        return most_occupied.record

    def most_occupied_in_a_row(self) -> int:
        """ Returns the most occupied cells in a row """
        return max(sum(1 for x in range(x_max) if self.guard_map[y][x] == '#') for y in range(y_max))

    def most_occupied_in_a_column(self) -> int:
        """ Returns the most occupied cells in a column """
        return max(sum(1 for y in range(y_max) if self.guard_map[y][x] == '#') for x in range(x_max))

    def unique_positions(self) -> int:
        """ Returns the number of unique positions """
        return sum(1 for p in self.positions() if self.occupied(p))

    def print(self) -> None:
        """ Print the guard map """
        for y in range(y_max):
            print(''.join(self.guard_map[y]))


def find_best(foo, minimize=False):
    record_keeper = RecordKeeper(minimize=minimize)
    guards = [
        Guard(Position(x, y), Position(vx, vy))
        for d in open('input.txt').read().strip().split('\n')
        for x, y, vx, vy in [map(int, re.findall(r'-?\d+', d))]
    ]

    # If the best value is found on multiple maps, I will print the alternative maps as well at the end.
    # (Printing alternatives during the search would be too verbose).
    best_maps = []

    # Due to the modular arithmetic, the x coordinates repeat every x_max and the y coordinates repeat every y_max
    # steps. Therefore, the grid will repeat every lcm(x_max, y_max) steps.
    # (Which happens to be 101 * 103 == 10403 in this case).
    for move_counter in range(math.lcm(x_max, y_max)):
        guard_map = GuardMap(guards)
        value = foo(guard_map)
        if record_keeper.update(value):
            print(f'Moves: {move_counter}')
            print(f'Value: {value}')
            guard_map.print()
            best_maps = []

        if record_keeper.record == value:
            best_maps.append((move_counter, guard_map))

        for guard in guards:
            guard.move()

    if len(best_maps) > 1:
        print('There were other maps with the same best value:')
        for i, best_map in range(1, len(best_maps)):
            print(f'Map {i}:')
            best_map.print()


# find_best(GuardMap.number_of_components, minimize=True)
# find_best(GuardMap.largest_component)
# find_best(GuardMap.most_occupied_in_a_row_consecutively)
# find_best(GuardMap.most_occupied_in_a_column_consecutively)
# find_best(GuardMap.most_occupied_in_a_row)  # This does NOT work on my input
# find_best(GuardMap.most_occupied_in_a_column)  # This DOES work on my input at least
find_best(GuardMap.unique_positions)  # Allegedly, for some inputs there are multiple grids with 500 unique positions
