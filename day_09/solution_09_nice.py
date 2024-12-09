from collections import deque
from dataclasses import dataclass
import typing


@dataclass
class File:
    position: int
    size: int
    value: int

@dataclass
class Space:
    position: int
    size: int

disk_map = open('input.txt').read().strip()
files: typing.List[File] = []
spaces: typing.List[Space] = []

position = 0
for i, c in enumerate(disk_map):
    size = int(c)
    if i % 2 == 0:
        files.append(File(position=position, size=size, value=i // 2))
    elif size > 0:
        spaces.append(Space(position=position, size=size))
    position += size

# Note that the files and the spaces are already sorted by their position.
assert files == sorted(files, key=lambda file: file.position)
assert spaces == sorted(spaces, key=lambda space: space.position)

# Part 1
class SpaceObserver:
    def __init__(self, spaces: typing.Deque[Space]):
        self.__spaces = spaces
        self.__space_index = 0
        self.__within_space_position = 0

    @property
    def position(self) -> int:
        """ The current position of the next free space. """
        return self.__spaces[self.__space_index].position + self.__within_space_position

    def occupy(self) -> None:
        """ Move the observer to the next free space. """
        self.__within_space_position += 1
        if self.__within_space_position >= self.__spaces[self.__space_index].size:
            self.__space_index += 1
            self.__within_space_position = 0

checksum = 0
observer = SpaceObserver(spaces)
for file in files[::-1]:
    for position in range(file.position + file.size - 1, file.position - 1, -1):
        if observer.position < position:
            checksum += observer.position * file.value
            observer.occupy()
        else:
            checksum += position * file.value
print(checksum)

# Part 2
class SpaceMultiObserver:
    def __init__(self, spaces: typing.Iterable[Space]):
        self.__spaces: typing.List[typing.Deque[int]] = [
            deque(space.position for space in spaces if space.size == size)
            for size in range(10)
        ]
        # Some safeguard for the case that there are no spaces of a certain size.
        big_number = sum(file.size for file in files)
        for space in self.__spaces:
            space.append(big_number)

    def position(self, at_least: int) -> typing.Tuple[int, int]:
        """ The current position of the next free space that is at least `at_least` long.

        Returns a tuple of the actual space size and the position of the space.
        The actual space size should be handed back to the `occupy` method.
        """
        space_size = min(range(at_least, len(self.__spaces)), key=lambda i: self.__spaces[i][0])
        return space_size, self.__spaces[space_size][0]

    def occupy(self, space_size: int, occupy_size: int) -> None:
        """ Occupy `occupy_size` space from the first space of size `space_size`.

        This means that there will be a new space of size `space_size - occupy_size` after the occupied place.
        """
        new_size = space_size - occupy_size
        if new_size > 0:
            self.__spaces[new_size].append(self.__spaces[space_size][0] + occupy_size)
            self.__spaces[new_size] = deque(sorted(self.__spaces[new_size]))
        self.__spaces[space_size].popleft()

checksum = 0
observer = SpaceMultiObserver(spaces)
for file in files[::-1]:
    space_size, position = observer.position(file.size)
    if position < file.position:
        checksum += file.value * sum(range(position, position + file.size))
        observer.occupy(space_size, file.size)
    else:
        checksum += file.value * sum(range(file.position, file.position + file.size))
print(checksum)
