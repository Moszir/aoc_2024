import re
import numpy
import scipy

integer_solutions = 0
numpy_inaccurate = 0
scipy_inaccurate = 0
both_inaccurate = 0


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def solve(a, b, prize):
    global integer_solutions, numpy_inaccurate, scipy_inaccurate, both_inaccurate
    result = (det(prize, b) / det(a, b), det(a, prize) / det(a, b))
    result2 = numpy.linalg.solve([[a[0], b[0]], [a[1], b[1]]], prize)
    result3 = scipy.linalg.solve([[a[0], b[0]], [a[1], b[1]]], prize)
    if all((x.is_integer() for x in result)):
        integer_solutions += 1
        both = 0
        if any((result[i].is_integer() != result2[i].is_integer() for i in (0, 1))):
            print(f'numpy inaccurate: {result[0]:10}, {result[1]:10} != {result2[0]:10}, {result2[1]:10}')
            numpy_inaccurate += 1
            both += 1
        if any((result[i].is_integer() != result3[i].is_integer() for i in (0, 1))):
            print(f'scipy inaccurate: {result[0]:10}, {result[1]:10} != {result3[0]:10}, {result3[1]:10}')
            scipy_inaccurate += 1
            both += 1
        if both == 2:
            both_inaccurate += 1


for d in open('input.txt').read().strip().split('\n\n'):
    a, b, prize = ([int(x) for x in re.findall(r'-?\d+', line)] for line in d.split('\n'))
    prize[0] += 1e13
    prize[1] += 1e13
    solve(a, b, prize)

print(f'integer solutions: {integer_solutions}')
print(f'numpy inaccurate: {numpy_inaccurate}')
print(f'scipy inaccurate: {scipy_inaccurate}')
print(f'scipy inaccurate: {both_inaccurate}')

# Output:
# ...
# numpy inaccurate: 119979134108.0, 125195618356.0 != 119979134108.00002, 125195618355.99997
# scipy inaccurate: 119979134108.0, 125195618356.0 != 119979134108.00002, 125195618355.99997
# numpy inaccurate: 223413762545.0, 116175156264.0 != 223413762545.0, 116175156264.00003
# scipy inaccurate: 223413762545.0, 116175156264.0 != 223413762545.0, 116175156264.00003
# numpy inaccurate: 204081632993.0, 116618075982.0 != 204081632993.0, 116618075982.00002
# scipy inaccurate: 204081632993.0, 116618075982.0 != 204081632993.0, 116618075982.00002
# integer solutions: 146
# numpy inaccurate: 55
# scipy inaccurate: 55
# scipy inaccurate: 55
