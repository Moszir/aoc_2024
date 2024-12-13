"""
This solution uses numpy and scipy to solve the system of equations.
It compares the results with the integer solution from the basic Python solution.
It shows that numpy and scipy are not accurate for this problem.
"""
import re
import numpy
import scipy

integer_solutions = 0
numpy_inaccurate = 0
scipy_inaccurate = 0
both_inaccurate = 0


def det(vector1, vector2):
    """ Calculates the determinant of a 2x2 matrix """
    return vector1[0] * vector2[1] - vector1[1] * vector2[0]


def solve(column1, column2, goal):
    """
    Solves the `[column1, column2] * [x, y] = goal` system of equations by:

    1. Cramer's rule
    2. numpy.linalg.solve
    3. scipy.linalg.solve

    If the solution is integer, it checks if numpy and scipy are accurate.
    Inaccuracies are printed, and counters are incremented.
    """
    global integer_solutions, numpy_inaccurate, scipy_inaccurate, both_inaccurate
    result = (det(goal, column2) / det(column1, column2), det(column1, goal) / det(column1, column2))

    matrix = numpy.linalg.matrix_transpose([column1, column2])
    result_np = numpy.linalg.solve(matrix, goal)
    result_sp = scipy.linalg.solve(matrix, goal)
    if all((x.is_integer() for x in result)):
        integer_solutions += 1
        both = 0
        if any((not result_np[i].is_integer() for i in (0, 1))):
            print(f'numpy inaccurate: {result[0]:10}, {result[1]:10} != {result_np[0]:10}, {result_np[1]:10}')
            numpy_inaccurate += 1
            both += 1
        if any((not result_sp[i].is_integer() for i in (0, 1))):
            print(f'scipy inaccurate: {result[0]:10}, {result[1]:10} != {result_sp[0]:10}, {result_sp[1]:10}')
            scipy_inaccurate += 1
            both += 1
        if both == 2:
            both_inaccurate += 1


for d in open('input.txt').read().strip().split('\n\n'):
    a, b, prize = ([int(x) for x in re.findall(r'-?\d+', line)] for line in d.split('\n'))
    prize[0] += 1e13
    prize[1] += 1e13
    solve(a, b, prize)

print(f'{integer_solutions=}')
print(f'{numpy_inaccurate=}')
print(f'{scipy_inaccurate=}')
print(f'{both_inaccurate=}')

# Output:
# ...
# numpy inaccurate: 119979134108.0, 125195618356.0 != 119979134108.00002, 125195618355.99997
# scipy inaccurate: 119979134108.0, 125195618356.0 != 119979134108.00002, 125195618355.99997
# numpy inaccurate: 223413762545.0, 116175156264.0 != 223413762545.0, 116175156264.00003
# scipy inaccurate: 223413762545.0, 116175156264.0 != 223413762545.0, 116175156264.00003
# numpy inaccurate: 204081632993.0, 116618075982.0 != 204081632993.0, 116618075982.00002
# scipy inaccurate: 204081632993.0, 116618075982.0 != 204081632993.0, 116618075982.00002
# integer_solutions=146
# numpy_inaccurate=55
# scipy_inaccurate=55
# scipy_inaccurate=55
