from collections import defaultdict

with open("input.txt", "r") as f:
    grid = f.read().splitlines()

key2locs = defaultdict(list)

for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] != ".":
            key2locs[grid[i][j]].append((i, j))

unique_locs = set()

for locs in key2locs.values():
    for i in range(len(locs)):
        for j in range(i + 1, len(locs)):
            x1, y1 = locs[i]
            x2, y2 = locs[j]
            # Get the locations of the two antinodes and check if they are in the grid
            x3, y3 = 2 * x2 - x1, 2 * y2 - y1
            x4, y4 = 2 * x1 - x2, 2 * y1 - y2
            if 0 <= x3 < len(grid) and 0 <= y3 < len(grid[0]):
                unique_locs.add((x3, y3))
            if 0 <= x4 < len(grid) and 0 <= y4 < len(grid[0]):
                unique_locs.add((x4, y4))

ans = len(unique_locs)
with open("part1.txt", "w") as f:
    f.write(str(ans))
                
# Part 2: More antinodes (as long as in the grid and in line with at least two antennas)
unique_locs = set()
for locs in key2locs.values():
    for i in range(len(locs)):
        for j in range(i + 1, len(locs)):
            x1, y1 = locs[i]
            x2, y2 = locs[j]
            # Get the locations of the all antinodes and check if they are in the grid
            dx, dy = x2 - x1, y2 - y1
            # Try increasing from x1, y1
            while True:
                x, y = x1 + dx, y1 + dy
                if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                    unique_locs.add((x, y))
                    x1, y1 = x, y
                else:
                    break
            # Try decreasing from x2, y2
            while True:
                x, y = x2 - dx, y2 - dy
                if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                    unique_locs.add((x, y))
                    x2, y2 = x, y
                else:
                    break

ans = len(unique_locs)
with open("part2.txt", "w") as f:
    f.write(str(ans))

