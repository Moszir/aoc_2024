""" Advent of Code Day 15

https://adventofcode.com/2024/day/15
"""
from collections import deque
import typing
import unittest


class Position(typing.NamedTuple):
    """ Represents a 2D position """
    row: int
    column: int

    def __add__(self, other: 'Position') -> 'Position':
        return Position(self.row + other.row, self.column + other.column)

    @staticmethod
    def right():
        return Position(0, 1)

    @staticmethod
    def left():
        return Position(0, -1)

    @staticmethod
    def up():
        return Position(-1, 0)

    @staticmethod
    def down():
        return Position(1, 0)


Connections = typing.Set[Position]
OptionalConnections = typing.Optional[Connections]


class Place:
    def __init__(
            self,
            blocking: bool = False,
            empty: bool = False,
            symbol: str = None,
            connected: OptionalConnections = None):
        self.blocking = blocking
        self.empty = empty
        self.connected = connected if connected is not None else set()
        self.symbol = symbol

    @staticmethod
    def create_blocker() -> 'Place':
        return Place(blocking=True, symbol='#')

    @staticmethod
    def create_empty() -> 'Place':
        return Place(empty=True, symbol='.')

    @staticmethod
    def create_connected(
            connected: OptionalConnections = None,
            symbol: str = 'O') -> 'Place':
        return Place(connected=connected, symbol=symbol)


class Grid:
    def __init__(self, rows: int, columns: int):
        self.grid = [[Place.create_empty() for _ in range(columns)] for _ in range(rows)]

    def __getitem__(self, item: Position) -> Place:
        return self.grid[item.row][item.column]

    def __setitem__(self, key: Position, value: Place):
        self.grid[key.row][key.column] = value

    def find_first(self, symbol: str) -> Position:
        return next((
            Position(_r, _c)
            for _r, row in enumerate(self.grid)
            for _c, _place in enumerate(row)
            if _place.symbol == symbol))

    def pushable(self, from_position: Position, direction: Position) -> typing.Tuple[bool, typing.Set[Position]]:
        to_be_processed = deque([from_position])
        to_be_pushed = set()
        pushable = True
        while to_be_processed:
            p = to_be_processed.popleft()
            if p in to_be_pushed:
                continue
            if not self[p].empty:
                to_be_pushed.add(p)

            q = p + direction
            if self[q].blocking:
                return False, set()
            elif not self[q].empty:
                to_be_processed.append(q)
            # else: empty space, nothing to do

            for connection in self[p].connected:
                to_be_processed.append(p + connection)
        return pushable, to_be_pushed

    def push(self, places: typing.Set[Position], direction: Position):
        _to_push = [(p, self[p]) for p in places]
        for p in places:
            self[p] = Place.create_empty()
        for p, place in _to_push:
            self[p + direction] = place

    def try_push(self, from_position: Position, direction: Position) -> bool:
        pushable, to_be_pushed = self.pushable(from_position, direction)
        if pushable:
            self.push(to_be_pushed, direction)
            return True
        return False

    def to_string_table(self) -> typing.List[str]:
        return [
            ''.join(p.symbol for p in row)
            for row in self.grid]

    @staticmethod
    def from_string_table(table: typing.List[str]) -> 'Grid':
        rows = len(table)
        columns = len(table[0])
        grid = Grid(rows, columns)
        for r, line in enumerate(table):
            for c, symbol in enumerate(line):
                p = Position(r, c)
                if symbol == '#':
                    grid[p] = Place.create_blocker()
                elif symbol == '.':
                    grid[p] = Place.create_empty()
                else:
                    grid[p] = Place.create_connected(symbol=symbol)
                    for direction in (Position.up(), Position.down(), Position.left(), Position.right()):
                        neighbor = p + direction
                        if 0 <= neighbor.row < rows and 0 <= neighbor.column < columns and table[neighbor.row][neighbor.column] == symbol:
                            grid[p].connected.add(direction)
        return grid


class TestSolution(unittest.TestCase):
    def test_part1(self):
        with open('input.txt') as f:
            lines1, lines2 = f.read().strip().split('\n\n')

        robot = None
        grid = Grid(rows=len(lines1.split('\n')), columns=len(lines1.split('\n')[0]))
        for r, line in enumerate(lines1.split('\n')):
            for c, place in enumerate(line):
                if place == '#':
                    grid.grid[r][c] = Place.create_blocker()
                elif place == '@':
                    grid.grid[r][c] = Place.create_empty()
                    robot = Position(r, c)
                elif place == '.':
                    grid.grid[r][c] = Place.create_empty()
                else:
                    grid.grid[r][c] = Place.create_connected(symbol=place)
        self.assertIsNotNone(robot)

        for c in ''.join(lines2.split('\n')):
            move = {
                '^': Position.up(),
                '>': Position.right(),
                'v': Position.down(),
                '<': Position.left()
            }[c]
            if grid.try_push(robot, move):
                robot += move

        self.assertEqual(
            1_463_512,
            sum(100 * r + c
                for r, row in enumerate(grid.grid)
                for c, t in enumerate(row)
                if t.symbol == 'O')
        )

    def test_part2(self):
        with open('input.txt') as f:
            lines1, lines2 = f.read().strip().split('\n\n')

        grid = Grid(
            rows=len(lines1.split('\n')),
            columns=len(lines1.split('\n')[0]) * 2)

        robot = None
        for r, line in enumerate(lines1.split('\n')):
            for c, place in enumerate(line):
                if place == '#':
                    grid.grid[r][2 * c] = Place.create_blocker()
                    grid.grid[r][2 * c + 1] = Place.create_blocker()
                elif place == '.':
                    grid.grid[r][2 * c] = Place.create_empty()
                    grid.grid[r][2 * c + 1] = Place.create_empty()
                elif place == '@':
                    grid.grid[r][2 * c] = Place.create_empty()
                    grid.grid[r][2 * c + 1] = Place.create_empty()
                    robot = Position(r, 2 * c)
                elif place == 'O':
                    grid.grid[r][2 * c] = Place.create_connected(symbol='[', connected={Position.right()})
                    grid.grid[r][2 * c + 1] = Place.create_connected(symbol=']', connected={Position.left()})
                else:
                    self.assertTrue(False)
        self.assertIsNotNone(robot)

        for c in ''.join(lines2.split('\n')):
            move = {
                '^': Position.up(),
                '>': Position.right(),
                'v': Position.down(),
                '<': Position.left()
            }[c]
            if grid.try_push(robot, move):
                robot += move

        self.assertEqual(
            1_486_520,
            sum(100 * r + c
                for r, row in enumerate(grid.grid)
                for c, t in enumerate(row)
                if t.symbol == '[')
        )

    def test_push_connected(self):
        grid = Grid.from_string_table([
            '.AA.....#',
            '..AAA...#',
            '.AA.BBB.#',
            '..A..B..#',
        ])

        # Push from 0, 0 to right
        self.assertTrue(grid.try_push(Position(0, 0), Position.right()))
        self.assertEqual(
            [
                '..AA....#',
                '...AAA..#',
                '..AABBB.#',
                '...A.B..#',
            ],
            grid.to_string_table())

        # Push again from 0, 0 to right. Nothing should change, we are pushing air.
        self.assertTrue(grid.try_push(Position(0, 0), Position.right()))
        self.assertEqual(
            [
                '..AA....#',
                '...AAA..#',
                '..AABBB.#',
                '...A.B..#',
            ],
            grid.to_string_table())

        # Push from 0, 1 to right. This time, the 'B' group should move too.
        self.assertTrue(grid.try_push(Position(0, 1), Position.right()))
        self.assertEqual(
            [
                '...AA...#',
                '....AAA.#',
                '...AABBB#',
                '....A.B.#',
            ],
            grid.to_string_table())

        # Push from 0, 2 to right. We should hit the wall via the 'B' group.
        self.assertFalse(grid.try_push(Position(0, 2), Position.right()))
        self.assertEqual(
            [
                '...AA...#',
                '....AAA.#',
                '...AABBB#',
                '....A.B.#',
            ],
            grid.to_string_table())


if __name__ == '__main__':
    unittest.main()

