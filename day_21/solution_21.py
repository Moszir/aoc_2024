""" Advent of Code Day 21"""
from collections import deque
from functools import cache
import itertools
import typing

lines = open('input.txt').read().splitlines()

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
                sequences[(key_from, key_to)] = ['A']
                continue

            possibilities = []
            to_be_processed = deque([(positions[key_from], '')])
            while to_be_processed:
                (r, c), moves = to_be_processed.popleft()
                for rr, cc, move in [(r - 1, c, '^'), (r + 1, c, 'v'), (r, c - 1, '<'), (r, c + 1, '>')]:
                    if 0 <= rr < len(keypad) and 0 <= cc < len(keypad[0]) and keypad[rr][cc] is not None:
                        if keypad[rr][cc] == key_to:
                            if possibilities and len(possibilities[-1]) < len(moves) + 1:
                                break
                            possibilities.append(moves + move + 'A')
                        else:
                            to_be_processed.append(((rr, cc), moves + move))
                else:
                    continue
                break
            sequences[(key_from, key_to)] = possibilities
    return sequences


my_sequences = calculate_sequences(my_keypad)
robot_sequences = calculate_sequences(robot_keypad)
robot_lengths = {key: len(value[0]) for key, value in robot_sequences.items()}


def steps(sequence: str) -> typing.Tuple[str, str]:
    """ Generate steps from 'A' """
    for _from, _to in zip('A' + sequence, sequence):
        yield _from, _to


@cache
def solve_sequence(sequence: str, depth_: int) -> int:
    """ Solve the sequence with the given depth """
    if depth_ == 1:
        return sum(robot_lengths[(x, y)] for x, y in steps(sequence))
    return sum((
        min(solve_sequence(subsequence, depth_ - 1) for subsequence in robot_sequences[(x, y)])
        for x, y in steps(sequence)))


def my_steps(line: str) -> str:
    """ Generates my possible steps for the given line. """
    my_possible_steps = [my_sequences[(x, y)] for x, y in steps(line)]
    for my_steps_ in itertools.product(*my_possible_steps):
        yield ''.join(my_steps_)


def solve_line(line, depth_):
    """ Solve the line with the given depth """
    return min((solve_sequence(my_steps_, depth_) for my_steps_ in my_steps(line)))


for depth in (2, 25):
    print(sum((int(line[:-1]) * solve_line(line, depth) for line in lines)))

# 270084
# 329431019997766
