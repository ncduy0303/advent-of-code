from collections import deque

W, H = 71, 71

with open("input.txt", "r") as f:
    coords = [tuple(map(int, reversed(line.strip().split(",")))) for line in f]

grid = [["."] * W for _ in range(H)]

for (i, j) in coords[:1024]:
    grid[i][j] = "#"

dist = [[0] * W for _ in range(H)]
grid[0][0] = "#"
que = deque([(0, 0)])
while que:
    i, j = que.popleft()
    for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < H and 0 <= nj < W and grid[ni][nj] == "." and dist[ni][nj] == 0:
            grid[ni][nj] = "#"
            dist[ni][nj] = dist[i][j] + 1
            que.append((ni, nj))

ans = dist[H - 1][W - 1]
with open("part1.txt", "w") as f:
    f.write(str(ans))

# Part 2: Find the first wall that will prevent the path from reaching the bottom right corner
# Grid size if small so just brute force it O(n^4)
for idx in range(1024, len(coords)):
    grid = [["."] * W for _ in range(H)]

    for (i, j) in coords[:idx + 1]:
        grid[i][j] = "#"

    dist = [[0] * W for _ in range(H)]
    grid[0][0] = "#"
    que = deque([(0, 0)])
    while que:
        i, j = que.popleft()
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < H and 0 <= nj < W and grid[ni][nj] == "." and dist[ni][nj] == 0:
                grid[ni][nj] = "#"
                dist[ni][nj] = dist[i][j] + 1
                que.append((ni, nj))

    if dist[H - 1][W - 1] == 0:
        ans = coords[idx]
        break

with open("part2.txt", "w") as f:
    f.write(f"{ans[1]},{ans[0]}")