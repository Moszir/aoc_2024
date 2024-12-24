""" Advent of Code Day 24 """
import typing

registers: typing.Set[str] = set()
values: typing.Dict[str, int] = {}  # The current value of the register
gates: typing.Dict[str, typing.Tuple[str, str, str]] = {}  # output <-> lhs, operation, rhs


def read():
    initial_values, gate_configurations = open('input.txt').read().strip().split('\n\n')
    for line in initial_values.split('\n'):
        reg, value = line.split(': ')
        values[reg] = int(value)
        registers.add(reg)

    for line in gate_configurations.split('\n'):
        lhs, operation, rhs, _, output_register = line.split()  # ignore the arrow
        gates[output_register] = (lhs, operation, rhs)
        registers.add(output_register)


def evaluate(register):
    if register in values:
        return values[register]
    op1 = evaluate(gates[register][0])
    op2 = evaluate(gates[register][2])
    if gates[register][1] == 'AND':
        return op1 & op2
    if gates[register][1] == 'OR':
        return op1 | op2
    if gates[register][1] == 'XOR':
        return op1 ^ op2


read()

digits = {}
for output in registers:
    if output.startswith('z'):
        digits[int(output[1:])] = evaluate(output)

result = 0
for i in range(max([k for k in digits]), -1, -1):
    result = 2 * result + digits[i]
print(result)  # 48508229772400
