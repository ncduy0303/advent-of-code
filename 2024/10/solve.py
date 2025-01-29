from collections import deque

with open("input.txt") as f:
    grid = [list(map(int, line.strip())) for line in f]

# Do a BFS from all cells with value 0
ans = 0 # Sum of number of cells with value 9 that are reachable from each cell with value 0
que = deque()
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == 0:
            que.append((i, j))
            reachable = set()
            while que:
                ci, cj = que.popleft()
                for ni, nj in [(ci-1, cj), (ci+1, cj), (ci, cj-1), (ci, cj+1)]:
                    if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                        if grid[ni][nj] == grid[ci][cj] + 1:
                            que.append((ni, nj))
                            if grid[ni][nj] == 9:
                                reachable.add((ni, nj))
            ans += len(reachable)

with open("part1.txt", "w") as f:
    f.write(str(ans))

# Part 2: Sum of distinct paths from any 0 to any 9
ans = 0
que = deque()
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == 0:
            que.append((i, j))
            while que:
                ci, cj = que.popleft()
                for ni, nj in [(ci-1, cj), (ci+1, cj), (ci, cj-1), (ci, cj+1)]:
                    if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                        if grid[ni][nj] == grid[ci][cj] + 1:
                            que.append((ni, nj))
                            if grid[ni][nj] == 9:
                                ans += 1

with open("part2.txt", "w") as f:
    f.write(str(ans))