import math, re
guards = [[x % 101, y % 103, vx % 101, vy % 103]
          for d in open('input.txt').read().strip().split('\n')
          for x, y, vx, vy in [map(int, re.findall(r'-?\d+', d))]]
best_round, lowest_safety_score = -1, 125 ** 4 + 1
for move in range(101 * 103):
    safety_score = math.prod([sum(1 for g in guards if sx * (g[0] - 101 // 2) > 0 and sy * (g[1] - 103 // 2) > 0)
                              for sx in [-1, 1] for sy in [-1, 1]])
    if safety_score < lowest_safety_score:
        best_round, lowest_safety_score = move, safety_score
    if move == 100:
        print(f'Part 1: {safety_score}')  # 214_109_808
    for g in guards:
        g[0], g[1] = (g[0] + g[2]) % 101, (g[1] + g[3]) % 103
print(f'Part 2: {best_round}')  # 7_687
