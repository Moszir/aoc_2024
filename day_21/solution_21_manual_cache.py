""" Advent of Code Day 21

Imagine that there are 1000 robots instead of 25...
Manual call stack, to get around the recursion limit.
Manual cache, because functools.cache no longer works without recursion.

Calculating the minimum number of steps for all 1000 possible input lines and writing them to a file
still takes less than 1 second.
"""
from collections import deque
import itertools
import typing


my_keypad = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A']]

robot_keypad = [
    [None, '^', 'A'],
    ['<', 'v', '>']]

Keypad = typing.List[typing.List[str]]
Sequences = typing.Dict[typing.Tuple[str, str], typing.List[str]]


def calculate_sequences(keypad: Keypad) -> Sequences:
    """ Calculate possible optimal sequences for each pair of keys """
    positions = {
        keypad[r][c]: (r, c)
        for r in range(len(keypad))
        for c in range(len(keypad[r]))
        if keypad[r][c] is not None}
    sequences = {}
    for key_from in positions:
        for key_to in positions:
            if key_from == key_to:
                # Press the big red button!
                sequences[(key_from, key_to)] = ['A']
                continue

            possibilities = []
            to_be_processed = deque([(positions[key_from], '')])
            while to_be_processed:
                (r, c), moves = to_be_processed.popleft()
                if possibilities and len(possibilities[-1]) < len(moves) + 1:
                    # It is a BFS, so if we have a shorter sequence than the current one,
                    # then all the other sequences in the queue lead to only longer sequences than what we already have.
                    break
                for rr, cc, move in [(r - 1, c, '^'), (r + 1, c, 'v'), (r, c - 1, '<'), (r, c + 1, '>')]:
                    if 0 <= rr < len(keypad) and 0 <= cc < len(keypad[0]) and keypad[rr][cc] is not None:
                        if keypad[rr][cc] == key_to:
                            possibilities.append(moves + move + 'A')
                        else:
                            to_be_processed.append(((rr, cc), moves + move))
            sequences[(key_from, key_to)] = possibilities
    return sequences


my_sequences = calculate_sequences(my_keypad)
robot_sequences = calculate_sequences(robot_keypad)


def steps(sequence: str) -> typing.Tuple[str, str]:
    """ Generate steps from 'A'

    For example: '249' |-> ('A', '2'), ('2', '4'), ('4', '9')
    """
    for _from, _to in zip('A' + sequence, sequence):
        yield _from, _to


def my_steps(line: str) -> str:
    """ Generates my possible steps for the given line.

    For example:
    line == '249' |-> ('A', '2'), ('2', '4'), ('4', '9')  # steps(line)
                  |-> [[p1, p2], [p3, p4, p5], [p6]]  # [my_sequences[(x, y)] for x, y in steps(line)]
                                                      # Here p1, p2 are possible sequences for 'A' -> '2'
                                                      # p3, p4, p5 are possible sequences for '2' -> '4'
                                                      # p6 is the only possible sequence for '4' -> '9'
                  |-> ((p1, p3, p6), (p1, p4, p6), (p1, p5, p6)
                       (p2, p3, p6), (p2, p4, p6), (p2, p5, p6))  # itertools.product(*my_possible_steps)
    # These are all the possible command sequences from 'A' to '9' that have a chance to be minimal.
    """
    my_possible_steps = [my_sequences[(x, y)] for x, y in steps(line)]
    for my_steps_ in itertools.product(*my_possible_steps):
        yield ''.join(my_steps_)

manual_cache = {}

def solve_line_with_manual_stack(line_: str, depth_: int) -> int:
    """ Solve the line with the given depth

    Simulate the call stack with a manual stack.
    """
    manual_stack = []
    for my_steps_ in my_steps(line_):
        if (my_steps_, depth_) not in manual_cache:
            manual_stack.append((my_steps_, depth_))

    while manual_stack:
        sequence, depth_ = manual_stack[-1]
        if (sequence, depth_) in manual_cache:
            manual_stack.pop()
            continue
        elif depth_ == 1:
            manual_cache[(sequence, depth_)] = sum(len(robot_sequences[(x, y)][0]) for x, y in steps(sequence))
            manual_stack.pop()
        else:
            if all((sub, depth_ - 1) in manual_cache for x, y in steps(sequence) for sub in robot_sequences[(x, y)]):
                manual_cache[(sequence, depth_)] = sum((
                    min(manual_cache[(subsequence, depth_ - 1)]
                        for subsequence in robot_sequences[(x, y)])
                    for x, y in steps(sequence)))
                manual_stack.pop()
            else:
                for x, y in steps(sequence):
                    for subsequence in robot_sequences[(x, y)]:
                        if (subsequence, depth_ - 1) not in manual_cache:
                            manual_stack.append((subsequence, depth_ - 1))
    return min((manual_cache[(my_steps_, depth_)] for my_steps_ in my_steps(line_)))


depth = 1_000
with open(f'output_{depth}.txt', 'w') as f:
    for d in range(1000):
        line = f'{d:03}A'
        print((line, (solve_line_with_manual_stack(line, depth))), file=f)

# To test that the results are the same as the recursive version
# lines = open('input.txt').read().splitlines()
# for depth in (2, 25):
#     print(sum((int(line[:-1]) * solve_line_with_manual_stack(line, depth) for line in lines)))
# 270084
# 329431019997766

# Cache lengths
print(f'Numeric keypad cache: {len(my_sequences)}')
print(f'Directional keypad cache: {len(robot_sequences)}')
print(f'Recursive cache: {len(manual_cache)}')
print(f'Total: {len(my_sequences) + len(robot_sequences) + len(manual_cache)}')
