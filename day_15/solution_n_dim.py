from collections import deque
import typing
import unittest


class Position(list):
    """ Represents a position in an n-dimensional grid. """

    def move(self, other: 'Position') -> 'Position':
        return Position([a + b for a, b in zip(self, other)])

    def __hash__(self):
        return hash(tuple(self))


# A cluster of positions in an n-dimensional grid.
Cluster = typing.Set[Position]
Clusters = typing.List[Cluster]
Blockers = typing.Set[Position]


def try_push(clusters: Clusters, blockers: Blockers, position: Position, move: Position) -> bool:
    if position in blockers:
        return False

    cluster_index = next((i for i in range(len(clusters)) if position in clusters[i]), None)
    if cluster_index is None:
        return True

    to_be_pushed = set()
    to_be_processed = deque([cluster_index])
    while to_be_processed:
        index = to_be_processed.popleft()
        if index in to_be_pushed:
            continue
        to_be_pushed.add(index)

        for p in clusters[index]:
            q = p.move(move)
            if q in blockers:
                return False
            q_cluster_index = next((c2 for c2 in range(len(clusters)) if q in clusters[c2]), None)
            if q_cluster_index is not None:
                to_be_processed.append(q_cluster_index)

    for c in to_be_pushed:
        clusters[c] = set(p.move(move) for p in clusters[c])
    return True



class Tests(unittest.TestCase):
    def test_part1(self):
        with open('input.txt') as f:
            lines1, lines2 = f.read().strip().split('\n\n')

        robot = None
        blockers = set()
        clusters = []
        for r, line in enumerate(lines1.split('\n')):
            for c, place in enumerate(line):
                if place == '#':
                    blockers.add(Position([r, c]))
                elif place == '@':
                    robot = Position([r, c])
                elif place != '.':
                    clusters.append({Position([r, c])})
        self.assertIsNotNone(robot)

        for c in ''.join(lines2.split('\n')):
            move = {
                '^': Position([-1, 0]),
                '>': Position([0, 1]),
                'v': Position([1, 0]),
                '<': Position([0, -1])
            }[c]
            if try_push(clusters, blockers, robot.move(move), move):
                robot = robot.move(move)

        self.assertEqual(
            1_463_512,
            sum(100 * p[0] + p[1] for c in clusters for p in c))

    def test_part2(self):
        with open('input.txt') as f:
            lines1, lines2 = f.read().strip().split('\n\n')

        robot = None
        blockers = set()
        clusters = []
        for r, line in enumerate(lines1.split('\n')):
            for c, place in enumerate(line):
                if place == '#':
                    blockers.add(Position([r, 2 * c]))
                    blockers.add(Position([r, 2 * c + 1]))
                elif place == '@':
                    robot = Position([r, 2 * c])
                elif place != '.':
                    clusters.append({Position([r, 2 * c]), Position([r, 2 * c + 1])})
        self.assertIsNotNone(robot)

        for c in ''.join(lines2.split('\n')):
            move = {
                '^': Position([-1, 0]),
                '>': Position([0, 1]),
                'v': Position([1, 0]),
                '<': Position([0, -1])
            }[c]
            if try_push(clusters, blockers, robot.move(move), move):
                robot = robot.move(move)

        self.assertEqual(
            1_486_520,
            sum(100 * min(p[0] for p in c) + min(p[1] for p in c)
                for c in clusters))


if __name__ == '__main__':
    unittest.main()
