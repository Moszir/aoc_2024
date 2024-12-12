import typing


class Position(typing.NamedTuple):
    row: int
    col: int

    def __add__(self, other: 'Position') -> 'Position':
        return Position(self.row + other.row, self.col + other.col)

    @staticmethod
    def directions():
        return Position(0, 1), Position(0, -1), Position(1, 0), Position(-1, 0)

    def neighbors(self):
        for d in self.directions():
            yield self + d


class Grid:
    def __init__(self, file_name: str):
        self.lines = open(file_name).read().strip().split('\n')
        self.rows = len(self.lines)
        self.cols = len(self.lines[0])

    def __in_bounds(self, position: Position) -> bool:
        return 0 <= position.row < self.rows and 0 <= position.col < self.cols

    def character(self, position: Position) -> str:
        return self.lines[position.row][position.col] if self.__in_bounds(position) else None

    def positions(self):
        for r in range(self.rows):
            for c in range(self.cols):
                yield Position(r, c)


class Component:
    def __init__(self, positions: typing.Set[Position] = None):
        self.positions = positions if positions is not None else set()

    def add(self, position: Position):
        self.positions.add(position)

    @property
    def area(self) -> int:
        return len(self.positions)

    @property
    def perimeter(self) -> int:
        return sum((
            1 if neighbor not in self.positions else 0
            for position in self.positions
            for neighbor in position.neighbors()))

    @property
    def corners(self) -> int:
        min_position = Position(min(_p.row for _p in self.positions), min(_p.col for _p in self.positions))
        max_position = Position(max(_p.row for _p in self.positions), max(_p.col for _p in self.positions))
        _corners = 0
        for _r in range(min_position.row - 1, max_position.row + 1):
            for _c in range(min_position.col - 1, max_position.col + 1):
                _p = Position(_r, _c)
                mask = [
                    _p                  in self.positions, _p + Position(0, 1) in self.positions,
                    _p + Position(1, 0) in self.positions, _p + Position(1, 1) in self.positions]
                _corners += (
                    1 if sum(mask) in (1, 3)  # a single 90 or 270-degree corner
                    else 2 if mask == [True, False, False, True] or mask == [False, True, True, False]  # two 90-degree corners touching
                    else 0)
        return _corners


grid = Grid('input.txt')
components: typing.List[Component] = []
for p in grid.positions():
    if any(p in component.positions for component in components):
        continue

    # We found a new group
    component = Component({p})
    components.append(component)

    character = grid.character(p)
    to_be_processed = {p}
    while to_be_processed:
        for n in to_be_processed.pop().neighbors():
            if grid.character(n) == character and n not in component.positions:
                component.add(n)
                to_be_processed.add(n)

print(f'Part 1: {sum(component.area * component.perimeter for component in components)}')  # 1396298
print(f'Part 2: {sum(component.area * component.corners for component in components)}')  # 853588
