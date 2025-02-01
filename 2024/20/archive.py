from typing import Tuple, List
from collections import deque

with open("input.txt", "r") as f:
    grid = [list(line.strip()) for line in f]

H, W = len(grid), len(grid[0])
start, end = None, None
for i in range(H):
    for j in range(W):
        if grid[i][j] == "S":
            start = (i, j)
        elif grid[i][j] == "E":
            end = (i, j)

# Run a BFS from start to end and return the shortest path length
def bfs(s: Tuple[int, int], e: Tuple[int, int]) -> List[List[int]]:
    que = deque([s])
    dist = [[-1] * W for _ in range(H)]
    dist[s[0]][s[1]] = 0
    while que:
        i, j = que.popleft()
        for ni, nj in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
            if 0 <= ni < H and 0 <= nj < W and grid[ni][nj] != "#" and dist[ni][nj] == -1:
                dist[ni][nj] = dist[i][j] + 1
                que.append((ni, nj))
    return dist

dist_s_old = bfs(start, end)
dist_e_old = bfs(end, start)
cost = dist_s_old[end[0]][end[1]]
ans = 0
# Try all possible cheating positions and count how many cheats reduce the cost by >= 100
for i in range(H):
    for j in range(W):
        if grid[i][j] == "#":
            pos = []
            # Iterate all 4 neighbors of the cheating position
            for ni, nj in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                if 0 <= ni < H and 0 <= nj < W and grid[ni][nj] != "#":
                    pos.append((ni, nj))
            if len(pos) < 2:
                continue

            grid[i][j] = "."
            dist_e = bfs(end, start)
            for ai, aj in pos:
                for bi, bj in pos:
                    if (ai, aj) == (bi, bj) or dist_s_old[ai][aj] == -1 or dist_e_old[bi][bj] == -1:
                        continue
                    # Check if the path from start to end can be shortened by 100
                    cur_cost = dist_s_old[ai][aj] + dist_e[bi][bj] + 2
                    if cost - cur_cost >= 100:
                        ans += 1
            grid[i][j] = "#"

with open("part1.txt", "w") as f:
    f.write(str(ans))