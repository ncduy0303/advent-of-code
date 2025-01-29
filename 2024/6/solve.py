from collections import deque

with open("input.txt", "r") as f:
    grid = [list(line.strip()) for line in f]

# Search for the "^" character
for i, row in enumerate(grid):
    for j, cell in enumerate(row):
        if cell == "^":
            start = (i, j)
            break

# Directions: 0 = up, 1 = right, 2 = down, 3 = left
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# Simulate the path with state = (row, col, direction)
cur = (start[0], start[1], 0)
loc = set()
vis = set()

while True:
    if cur in vis:
        break
    vis.add(cur)
    loc.add(cur[:2])

    # Try to move forward
    new = (cur[0] + directions[cur[2]][0], cur[1] + directions[cur[2]][1], cur[2])
    
    # If out of grid, break
    if new[0] < 0 or new[0] >= len(grid) or new[1] < 0 or new[1] >= len(grid[0]):
        break

    # If wall, turn right
    if grid[new[0]][new[1]] == "#":
        new = (cur[0], cur[1], (cur[2] + 1) % 4)

    cur = new

# Number of unique locations visited
ans = len(loc)

with open("part1.txt", "w") as f:
    f.write(str(ans))


# Part 2: Count number of ways to put only 1 wall to make it unable to exit the grid
# Just brute force all possible walls and check if it's possible to exit the grid
ans = 0

for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == ".":
            print(i, j)
            # Try to put a wall here
            grid[i][j] = "#"

            # Simulate the traversal
            cur = (start[0], start[1], 0)
            loc = set()
            vis = set()

            while True:
                if cur in vis:
                    ans += 1
                    break
                vis.add(cur)
                loc.add(cur[:2])

                # Try to move forward
                new = (cur[0] + directions[cur[2]][0], cur[1] + directions[cur[2]][1], cur[2])
                
                # If out of grid, break
                if new[0] < 0 or new[0] >= len(grid) or new[1] < 0 or new[1] >= len(grid[0]):
                    break

                # If wall, turn right
                if grid[new[0]][new[1]] == "#":
                    new = (cur[0], cur[1], (cur[2] + 1) % 4)

                cur = new

            # Reset the state
            grid[i][j] = "."

with open("part2.txt", "w") as f:
    f.write(str(ans))