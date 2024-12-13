from scipy import optimize


results = []
for d in open('input.txt').read().strip().split('\n\n'):
    lines = d.split('\n')
    a_x = int(lines[0].split(',')[0].split('+')[1])
    a_y = int(lines[0].split(',')[1].split('+')[1])
    b_x = int(lines[1].split(',')[0].split('+')[1])
    b_y = int(lines[1].split(',')[1].split('+')[1])
    prize_x = int(lines[2].split(',')[0].split('=')[1]) + 10000000000000
    prize_y = int(lines[2].split(',')[1].split('=')[1]) + 10000000000000
    result = optimize.milp(
        c=[3, 1],
        constraints=[
            optimize.LinearConstraint(
                A=[a_x, b_x],
                lb=prize_x,
                ub=prize_x),
            optimize.LinearConstraint(
                A=[a_y, b_y],
                lb=prize_y,
                ub=prize_y)],
        bounds=optimize.Bounds(lb=0),
        integrality=True)
    if result.success:
        results.append(result)

print(sum([result.fun for result in results]))
