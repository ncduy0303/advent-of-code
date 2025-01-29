import re

cost_a = 3
cost_b = 1
n = 320
pattern_button = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")
pattern_prize = re.compile(r"Prize: X=(\d+), Y=(\d+)")

ans = 0

with open("input.txt", "r") as f:
    for _ in range(n):
        button_a = tuple(map(int, pattern_button.match(f.readline()).groups()))
        button_b = tuple(map(int, pattern_button.match(f.readline()).groups()))
        prize = tuple(map(int, pattern_prize.match(f.readline()).groups()))
        f.readline() # empty line

        for b in range(101):
            for a in range(101):
                if prize[0] == button_a[0] * a + button_b[0] * b and prize[1] == button_a[1] * a + button_b[1] * b:
                    ans += cost_a * a + cost_b * b
                    break

with open("part1.txt", "w") as f:
    f.write(str(ans))

# Part 2: Not guaranteed to be solvable with <= 100 buttons
ans = 0
with open("input.txt", "r") as f:
    for _ in range(n):
        button_a = tuple(map(int, pattern_button.match(f.readline()).groups()))
        button_b = tuple(map(int, pattern_button.match(f.readline()).groups()))
        prize = tuple(map(int, pattern_prize.match(f.readline()).groups()))
        prize = (prize[0] + 10000000000000, prize[1] + 10000000000000)
        f.readline() # empty line

        # 2 equations, 2 unknowns -> just solve it
        # prize[0] = button_a[0] * a + button_b[0] * b
        # prize[1] = button_a[1] * a + button_b[1] * b
        det = button_a[0] * button_b[1] - button_a[1] * button_b[0]
        a = (prize[0] * button_b[1] - prize[1] * button_b[0]) / det
        b = (button_a[0] * prize[1] - button_a[1] * prize[0]) / det
        # Only consider non-negative integer solutions
        if a >= 0 and b >= 0 and a == int(a) and b == int(b):
            ans += cost_a * int(a) + cost_b * int(b)

with open("part2.txt", "w") as f:
    f.write(str(ans))