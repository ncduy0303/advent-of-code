from collections import deque, defaultdict

with open("input.txt", "r")  as f:
    grid = f.read().splitlines()

# Do a BFS to find the area and perimeter of each connected component
ans = 0
vis = [[False] * len(grid[0]) for _ in range(len(grid))]
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if not vis[i][j]:
            que = deque([(i, j)])
            vis[i][j] = True
            area, perimeter = 0, 0
            while que:
                x, y = que.popleft()
                area += 1
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and not vis[nx][ny] and grid[nx][ny] == grid[i][j]:
                        vis[nx][ny] = True
                        que.append((nx, ny))
                    if nx == -1 or nx == len(grid) or ny == -1 or ny == len(grid[0]) or grid[nx][ny] != grid[i][j]:
                        perimeter += 1
            ans += area * perimeter

with open("part1.txt", "w") as f:
    f.write(str(ans))

# Part 2: Perimeter is changed to the number of sides of the connected component (adjacent perimeter is grouped together to form a single side)
ans = 0
vis = [[False] * len(grid[0]) for _ in range(len(grid))]
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if not vis[i][j]:
            que = deque([(i, j)])
            vis[i][j] = True
            fences = defaultdict(lambda: defaultdict(list))
            area, side = 0, 0
            while que:
                x, y = que.popleft()
                area += 1
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and not vis[nx][ny] and grid[nx][ny] == grid[i][j]:
                        vis[nx][ny] = True
                        que.append((nx, ny))
                    if nx == -1 or nx == len(grid) or ny == -1 or ny == len(grid[0]) or grid[nx][ny] != grid[i][j]:
                        if dx == 0:
                            # Vertical fence
                            fences[(dx, dy)][y].append(x)
                        else:
                            # Horizontal fence
                            fences[(dx, dy)][x].append(y)
            for _, fence in fences.items():
                for _, points in fence.items():
                    arr = sorted(points)
                    side += 1
                    for k in range(1, len(arr)):
                        if arr[k] - arr[k - 1] > 1:
                            side += 1
            ans += area * side

with open("part2.txt", "w") as f:
    f.write(str(ans))