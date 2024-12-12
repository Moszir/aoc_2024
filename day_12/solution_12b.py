""" Advent of Code Day 12

https://adventofcode.com/2024/day/12
"""
import typing
import unittest


class Position(typing.NamedTuple):
    """ Represents a position in a grid. """
    row: int
    col: int

    def __add__(self, other: 'Position') -> 'Position':
        return Position(self.row + other.row, self.col + other.col)

    @staticmethod
    def directions():
        """ The four cardinal directions. """
        return Position(0, 1), Position(0, -1), Position(1, 0), Position(-1, 0)

    def neighbors(self):
        """ Generates the four neighbors of the position. """
        for d in self.directions():
            yield self + d


class Grid:
    """ Represents a grid of characters. """

    def __init__(self, file_name: str):
        with open(file_name) as f:
            self.__lines = f.read().strip().split('\n')
            self.__rows = len(self.__lines)
            self.__cols = len(self.__lines[0])

    def __in_bounds(self, position: Position) -> bool:
        return 0 <= position.row < self.__rows and 0 <= position.col < self.__cols

    def __getitem__(self, position: Position) -> typing.Optional[str]:
        """ Returns the character at the given position, or None if the position is out of bounds. """
        return self.__lines[position.row][position.col] if self.__in_bounds(position) else None

    def positions(self):
        """ Generates all positions in the grid.

        So we don't have to use a nested loop to iterate over all positions.
        """
        for r in range(self.__rows):
            for c in range(self.__cols):
                yield Position(r, c)


class Component(set):
    """ Represents a connected component of a grid. """

    @property
    def area(self) -> int:
        """ Calculates the area of the component. """
        return len(self)

    @property
    def perimeter(self) -> int:
        """ Calculates the perimeter of the component. """
        return sum((
            1 if neighbor not in self else 0
            for position in self
            for neighbor in position.neighbors()))

    @property
    def corners(self) -> int:
        """ Counts the number of corners of the component. """
        min_position = Position(min(_p.row for _p in self), min(_p.col for _p in self))
        max_position = Position(max(_p.row for _p in self), max(_p.col for _p in self))
        _corners = 0
        for _r in range(min_position.row - 1, max_position.row + 1):
            for _c in range(min_position.col - 1, max_position.col + 1):
                _p = Position(_r, _c)
                mask = [
                    _p + _d in self
                    for _d in (Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1))]
                _corners += (
                    # a single 90 or 270-degree corner:
                    1 if sum(mask) in (1, 3)
                    # or 2 corners meeting diagonally:
                    else 2 if mask == [True, False, False, True] or mask == [False, True, True, False]
                    # Otherwise no corner (4 misses, 4 hits, or 2 hits that are just an edge)
                    else 0)
        return _corners


def solve(file_name: str) -> typing.Tuple[int, int]:
    """ Solves both parts of the puzzle for the given input file. """
    grid = Grid(file_name)
    components: typing.List[Component] = []
    for p in grid.positions():
        if any(p in component for component in components):
            continue

        # We found a new group
        component = Component({p})
        components.append(component)

        character = grid[p]
        to_be_processed = {p}
        while to_be_processed:
            for n in to_be_processed.pop().neighbors():
                if grid[n] == character and n not in component:
                    component.add(n)
                    to_be_processed.add(n)

    return (
        sum(component.area * component.perimeter for component in components),
        sum(component.area * component.corners for component in components))


class TestSolution(unittest.TestCase):
    def __test_input(self, file_name: str, expected_part1: int, expected_part2: int) -> None:
        self.assertEqual(solve(file_name), (expected_part1, expected_part2))

    def __test_part2(self, file_name: str, expected: int) -> None:
        self.assertEqual(solve(file_name)[1], expected)

    def test_example_1(self):
        self.__test_input('ex_1.txt', 140, 80)

    def test_example_2(self):
        self.__test_input('ex_2_holes.txt', 772, 436)

    def test_example_3(self):
        self.__test_input('ex_3.txt', 1_930, 1_206)

    def test_example_4(self):
        self.__test_part2('ex_4_shape_e.txt', 236)

    def test_example_5(self):
        self.__test_part2('ex_5_no_mobius.txt', 368)

    def test_real_input(self):
        self.__test_input('input.txt', 1_396_298, 853_588)


if __name__ == '__main__':
    unittest.main()
