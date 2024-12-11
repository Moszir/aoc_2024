import dataclasses
import typing


lines = open('input.txt').read().strip().split('\n')
rows = len(lines)
cols = len(lines[0])

Position = typing.Tuple[int, int]

@dataclasses.dataclass
class Place:
    place: Position
    score: int
    peaks: typing.Set[Position]

    @property
    def neighbors(self) -> typing.Iterable[Position]:
        return (
            (self.place[0] + dr, self.place[1] + dc)
            for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)])


places = { height: [] for height in range(10) }
for r, row in enumerate(lines):
    for c, height in enumerate(row):
        places[int(height)].append(Place((r, c), 0, set()))

for place in places[9]:
    place.peaks = set(place.place,)
    place.score = 1

for height in range(8, -1, -1):
    for place in places[height]:
        for r, c in place.neighbors:
            if 0 <= r < rows and 0 <= c < cols and lines[r][c] == str(height + 1):
                neighbor = next(p for p in places[height + 1] if p.place == (r, c))
                place.peaks.update(neighbor.peaks)
                place.score += neighbor.score

print(sum(len(place.peaks) for place in places[0]))  # 1021
print(sum(place.score for place in places[0]))  # 1302
