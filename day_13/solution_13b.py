"""

Advent of Code

    [About][Events][Shop][Settings][Log Out]

Richárd Molnár-Szipai 25*
       λy.2024

    [Calendar][AoC++][Sponsors][Leaderboard][Stats]

--- Day 13: Claw Contraption ---

Next up: the lobby of a resort on a tropical island. The Historians take a moment to admire the hexagonal floor tiles before spreading out.

Fortunately, it looks like the resort has a new arcade! Maybe you can win some prizes from the claw machines?

The claw machines here are a little unusual. Instead of a joystick or directional buttons to control the claw, these machines have two buttons labeled A and B. Worse, you can't just put in a token and play; it costs 3 tokens to push the A button and 1 token to push the B button.

With a little experimentation, you figure out that each machine's buttons are configured to move the claw a specific amount to the right (along the X axis) and a specific amount forward (along the Y axis) each time that button is pressed.

Each machine contains one prize; to win the prize, the claw must be positioned exactly above the prize on both the X and Y axes.

You wonder: what is the smallest number of tokens you would have to spend to win as many prizes as possible? You assemble a list of every machine's button behavior and prize location (your puzzle input). For example:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279

This list describes the button configuration and prize location of four different claw machines.

For now, consider just the first claw machine in the list:

    Pushing the machine's A button would move the claw 94 units along the X axis and 34 units along the Y axis.
    Pushing the B button would move the claw 22 units along the X axis and 67 units along the Y axis.
    The prize is located at X=8400, Y=5400; this means that from the claw's initial position, it would need to move exactly 8400 units along the X axis and exactly 5400 units along the Y axis to be perfectly aligned with the prize in this machine.

The cheapest way to win the prize is by pushing the A button 80 times and the B button 40 times. This would line up the claw along the X axis (because 80*94 + 40*22 = 8400) and along the Y axis (because 80*34 + 40*67 = 5400). Doing this would cost 80*3 tokens for the A presses and 40*1 for the B presses, a total of 280 tokens.

For the second and fourth claw machines, there is no combination of A and B presses that will ever win a prize.

For the third claw machine, the cheapest way to win the prize is by pushing the A button 38 times and the B button 86 times. Doing this would cost a total of 200 tokens.

So, the most prizes you could possibly win is two; the minimum tokens you would have to spend to win all (two) prizes is 480.

You estimate that each button would need to be pressed no more than 100 times to win a prize. How else would someone be expected to play?

Figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?

Your puzzle answer was 35082.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

As you go to win the first prize, you discover that the claw is nowhere near where you expected it would be. Due to a unit conversion error in your measurements, the position of every prize is actually 10000000000000 higher on both the X and Y axis!

Add 10000000000000 to the X and Y position of every prize. After making this change, the example above would now look like this:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279

Now, it is only possible to win a prize on the second and fourth claw machines. Unfortunately, it will take many more than 100 presses to do so.

Using the corrected prize coordinates, figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?
"""
from fractions import Fraction

def check_solution(a_moves, b_moves, target_x, target_y, ax, ay, bx, by):
    x = a_moves * ax + b_moves * bx
    y = a_moves * ay + b_moves * by
    return x == target_x and y == target_y

def find_min_tokens(ax, ay, bx, by, target_x, target_y, part2=False):
    if not part2:
        # Part 1: brute force up to 100 moves
        for total_moves in range(201):
            for a_moves in range(total_moves + 1):
                b_moves = total_moves - a_moves
                if a_moves > 100 or b_moves > 100:
                    continue
                if check_solution(a_moves, b_moves, target_x, target_y, ax, ay, bx, by):
                    return 3 * a_moves + b_moves
        return None
    else:
        # Part 2: solve using linear equations
        # ax*A + bx*B = target_x
        # ay*A + by*B = target_y
        try:
            # Convert to fractions to handle large numbers
            det = ax * by - ay * bx
            if det == 0:
                return None

            a_moves = Fraction(target_x * by - target_y * bx, det)
            b_moves = Fraction(ax * target_y - ay * target_x, det)

            # Check if solution is integer and non-negative
            if (a_moves.denominator == 1 and b_moves.denominator == 1 and
                a_moves >= 0 and b_moves >= 0):
                return 3 * int(a_moves) + int(b_moves)
        except:
            pass
        return None

def solve_parts(data, part2=False):
    total_tokens = 0
    offset = 10000000000000 if part2 else 0

    machines = data.strip().split('\n\n')
    for machine in machines:
        lines = machine.strip().split('\n')
        ax = int(lines[0].split('X+')[1].split(',')[0])
        ay = int(lines[0].split('Y+')[1])
        bx = int(lines[1].split('X+')[1].split(',')[0])
        by = int(lines[1].split('Y+')[1])
        target_x = int(lines[2].split('X=')[1].split(',')[0]) + offset
        target_y = int(lines[2].split('Y=')[1]) + offset

        tokens = find_min_tokens(ax, ay, bx, by, target_x, target_y, part2)
        if tokens is not None:
            total_tokens += tokens

    return total_tokens

input_data = open('input.txt').read().strip()

result1 = solve_parts(input_data)
print(f"Part 1: {result1}")

result2 = solve_parts(input_data, part2=True)
print(f"Part 2: {result2}")
