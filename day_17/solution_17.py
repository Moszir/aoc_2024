import dataclasses
import re

lines1, lines2 = open('input.txt').read().strip().split('\n\n')
A, B, C = [int(x) for x in re.findall(r'-?\d+', lines1)]
program = [int(x) for x in re.findall(r'-?\d+', lines2)]


@dataclasses.dataclass
class Device:
    a: int
    b: int
    c: int

    def __init__(self):
        self.a = 0
        self.b = 0
        self.c = 0

    def solve(self, a: int):
        """ Simulate the device with the given program and initial value of register A. """
        self.a = a
        self.b = 0
        self.c = 0
        ip = 0
        output = []
        global program

        while ip < len(program):
            command = program[ip]
            op = program[ip + 1]
            combo = [0, 1, 2, 3, self.a, self.b, self.c, -1][op]

            if command == 0:  # adv, division
                self.a = self.a // 2 ** combo
            elif command == 1:  # bxl, xor
                self.b ^= op
            elif command == 2:  # bst, combo mod 8
                self.b = combo % 8
            elif command == 3:  # jnz, jump if a != 0
                if self.a != 0:
                    ip = op
                    continue
            elif command == 4:  # bxc, b = b ^ c
                self.b ^= self.c
            elif command == 5:  # out, output combo mod 8
                output.append(int(combo % 8))
            elif command == 6:  # bdv, adv just stored in b
                self.b = self.a // 2 ** combo
            elif command == 7:  # cdv, adv just stored in c
                self.c = self.a // 2 ** combo
            ip += 2
        return output


device = Device()
print(','.join([str(x) for x in device.solve(A)]))


def recursive_run(n, a):
    if n == -1:
        return a
    a <<= 3
    for x in range(8):
        if device.solve(a + x) == program[n:]:
            s = recursive_run(n - 1, a + x)
            if s != -1:
                return s
    return -1


print(recursive_run(len(program) - 1, 0))
# 267265166222235
