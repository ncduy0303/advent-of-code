import re
from collections import defaultdict

# Count the number of times "XMAS" appears in the file (horizontal, vertical, diagonal, can be backwards and overlapping)
# pattern = re.compile(r"XMAS|SAMX")
pattern1 = re.compile(r"XMAS")
pattern2 = re.compile(r"SAMX")

ans = 0

with open("input.txt", "r") as f:
    grid = f.read().splitlines()

# Horizontal
ans += sum(len(pattern1.findall(row)) for row in grid)
ans += sum(len(pattern2.findall(row)) for row in grid)

# Vertical
ans += sum(len(pattern1.findall("".join(col))) for col in zip(*grid))
ans += sum(len(pattern2.findall("".join(col))) for col in zip(*grid))

# Diagonal
diag1, diag2 = defaultdict(list), defaultdict(list)
for i in range(len(grid)):
    for j in range(len(grid[i])):
        diag1[i-j].append(grid[i][j])
        diag2[i+j].append(grid[i][j])
ans += sum(len(pattern1.findall("".join(diag))) for diag in diag1.values())
ans += sum(len(pattern2.findall("".join(diag))) for diag in diag1.values())
ans += sum(len(pattern1.findall("".join(diag))) for diag in diag2.values())
ans += sum(len(pattern2.findall("".join(diag))) for diag in diag2.values())

with open("part1.txt", "w") as f:
    f.write(str(ans))

# Part 2: Count the number of 3x3 squares that have 2 "MAS" in the two diagonals

ans = 0

for i in range(len(grid)-2):
    for j in range(len(grid[i])-2):
        str1 = grid[i][j] + grid[i+1][j+1] + grid[i+2][j+2]
        str2 = grid[i][j+2] + grid[i+1][j+1] + grid[i+2][j]
        if str1 in ["MAS", "SAM"] and str2 in ["MAS", "SAM"]:
            ans += 1

with open("part2.txt", "w") as f:
    f.write(str(ans))