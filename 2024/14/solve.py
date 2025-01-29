import re
from collections import defaultdict
import matplotlib.pyplot as plt

X, Y = 101, 103
turn = 100
pattern = re.compile(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)')

def get_quad(x: int, y: int) -> int:
    XC, XY = X // 2, Y // 2
    if x == XC or y == XY:
        return -1
    return (x >= XC) + 2 * (y >= XY)

with open("input.txt", "r") as f:
    robots = [list(map(int, pattern.match(line).groups())) for line in f]

quad2robots = defaultdict(int)

for robot in robots:
    x, y, vx, vy = robot
    nx, ny = x + vx * turn, y + vy * turn
    # Wrap around
    nx %= X
    ny %= Y
    if nx < 0:
        nx += X
    if ny < 0:
        ny += Y
    quad2robots[get_quad(nx, ny)] += 1

# Product of the number of robots in each quadrant
ans = 1
for quad, cnt in quad2robots.items():
    if quad != -1:
        ans *= cnt

with open("part1.txt", "w") as f:
    f.write(str(ans))

# Part 2: Guess the number of turns for the robots to arrange themselves into a Christmas tree
turn = 8000
regions = [0] * turn
for idx in range(turn):
    grid = [[0] * Y for _ in range(X)]
    for robot in robots:
        x, y, vx, vy = robot
        nx, ny = x + vx * idx, y + vy * idx
        nx %= X
        ny %= Y
        if nx < 0:
            nx += X
        if ny < 0:
            ny += Y
        grid[nx][ny] += 1
    # Do a BFS to count the number of connected components
    visited = [[False] * Y for _ in range(X)]
    for x in range(X):
        for y in range(Y):
            if grid[x][y] == 0 or visited[x][y]:
                continue
            regions[idx] += 1
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                visited[cx][cy] = True
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < X and 0 <= ny < Y and grid[nx][ny] > 0 and not visited[nx][ny]:
                        stack.append((nx, ny))

# Plot the number of connected components over time
plt.plot(range(turn), regions)
plt.xlabel("Time")
plt.ylabel("Number of connected components")
plt.savefig("part2.png")
plt.close()

# Take the index of the minimum number of connected components
turn = regions.index(min(regions))
print(f"Minimum number of connected components at time {turn} with {min(regions)} components")

# Display the arrangement
grid = [["."] * Y for _ in range(X)]
for robot in robots:
    x, y, vx, vy = robot
    nx, ny = x + vx * turn, y + vy * turn
    nx %= X
    ny %= Y
    if nx < 0:
        nx += X
    if ny < 0:
        ny += Y
    grid[nx][ny] = "X"

with open("tree.txt", "w") as f:
    f.write("\n".join("".join(row) for row in grid))

with open("part2.txt", "w") as f:
    f.write(str(turn))