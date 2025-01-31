from heapq import heappop, heappush

with open("input.txt", "r") as f:
    grid = f.read().splitlines()

# right, down, left, up
rot = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Find the start and end points
start = None
end = None
for i, row in enumerate(grid):
    for j, cell in enumerate(row):
        if cell == "S":
            start = (i, j, 0) # facing right at the start
        elif cell == "E":
            end = (i, j, -1) # doesn't matter which way we're facing at the end

# Dijkstra's algorithm
pq = [(0, start)]
dist = {start: 0}
while pq:
    d, (i, j, k) = heappop(pq)
    if d > dist[(i, j, k)]:
        continue
    ni, nj = i - rot[k][0], j - rot[k][1]
    if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]) and grid[ni][nj] != "#":
        if (ni, nj, k) not in dist or d + 1 < dist[(ni, nj, k)]:
            dist[(ni, nj, k)] = d + 1
            heappush(pq, (d + 1, (ni, nj, k)))
    # Rotate left or right
    if (i, j, (k + 1) % 4) not in dist or d + 1000 < dist[(i, j, (k + 1) % 4)]:
        dist[(i, j, (k + 1) % 4)] = d + 1000
        heappush(pq, (d + 1000, (i, j, (k + 1) % 4)))
    if (i, j, (k - 1) % 4) not in dist or d + 1000 < dist[(i, j, (k - 1) % 4)]:
        dist[(i, j, (k - 1) % 4)] = d + 1000
        heappush(pq, (d + 1000, (i, j, (k - 1) % 4)))
    # Special case: ending cell (doesn't matter which way we're facing)
    if (i, j, -1) == end:
        if (i, j, -1) not in dist or d < dist[(i, j, -1)]:
            dist[(i, j, -1)] = d

ans = dist[end]
with open("part1.txt", "w") as f:
    f.write(str(ans))

# Count the number of unique cells on the shortest path from start to end
# Dijkstra's algorithm from end
pq = [(0, end)]
dist2 = {end: 0}
while pq:
    d, (i, j, k) = heappop(pq)
    if d > dist2[(i, j, k)]:
        continue

    if (i, j, k) == end:
        for k in range(4):
            dist2[(i, j, k)] = 0
            heappush(pq, (0, (i, j, k)))
        continue

    ni, nj = i + rot[k][0], j + rot[k][1]
    if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]) and grid[ni][nj] != "#":
        if (ni, nj, k) not in dist2 or d + 1 < dist2[(ni, nj, k)]:
            dist2[(ni, nj, k)] = d + 1
            heappush(pq, (d + 1, (ni, nj, k)))
    # Rotate left or right
    if (i, j, (k + 1) % 4) not in dist2 or d + 1000 < dist2[(i, j, (k + 1) % 4)]:
        dist2[(i, j, (k + 1) % 4)] = d + 1000
        heappush(pq, (d + 1000, (i, j, (k + 1) % 4)))
    if (i, j, (k - 1) % 4) not in dist2 or d + 1000 < dist2[(i, j, (k - 1) % 4)]:
        dist2[(i, j, (k - 1) % 4)] = d + 1000
        heappush(pq, (d + 1000, (i, j, (k - 1) % 4)))

ans = 0
for i in range(len(grid)):
    for j in range(len(grid[0])):
        for k in range(4):
            if (i, j, k) in dist and (i, j, k) in dist2 and dist[(i, j, k)] + dist2[(i, j, k)] == dist[end]:
                ans += 1
                break

with open("part2.txt", "w") as f:
    f.write(str(ans))