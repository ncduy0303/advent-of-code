# 162,817,812
# 57,618,57
# 906,360,560
# 592,479,940
# 352,342,300
# 466,668,158
# 542,29,236
# 431,825,988
# 739,650,466
# 52,470,668
# 216,146,977
# 819,987,18
# 117,168,530
# 805,96,715
# 346,949,466
# 970,615,88
# 941,993,340
# 862,61,35
# 984,92,344
# 425,690,689
with open("input.txt") as f:
    # Read the input into a list of (x, y, z) tuples
    points: list[tuple[int, int, int]] = []
    for line in f.readlines():
        x, y, z = map(int, line.strip().split(','))
        points.append((x, y, z))

# Part 1: connect together the 1000 pairs of junction boxes which are closest together. 
# Afterward, what do you get if you multiply together the sizes of the three largest circuits?
# Use min-heap to efficiently get the 1000 closest pairs
# Use DSU to manage connected components
from heapq import heappush_max, heappop_max

def solve_part1(points: list[tuple[int, int, int]]) -> int:
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = sum((points[i][k] - points[j][k]) ** 2 for k in range(3))
            heappush_max(edges, (dist, i, j))
            if len(edges) > 1000:
                heappop_max(edges)

    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            if size[rootX] < size[rootY]:
                rootX, rootY = rootY, rootX
            parent[rootY] = rootX
            size[rootX] += size[rootY]

    for dist, u, v in edges:
        union(u, v)

    component_sizes = {}
    for i in range(n):
        root = find(i)
        if root not in component_sizes:
            component_sizes[root] = 0
        component_sizes[root] += 1

    largest_sizes = sorted(component_sizes.values(), reverse=True)[:3]
    result = 1
    for s in largest_sizes:
        result *= s

    return result

with open("part1.txt", "w") as f:
    f.write(str(solve_part1(points)))

# Part 2: Continue connecting the closest unconnected pairs of junction boxes together until they're all in the same circuit. 
# What do you get if you multiply together the X coordinates of the last two junction boxes you need to connect?
def solve_part2(points: list[tuple[int, int, int]]) -> int:
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = sum((points[i][k] - points[j][k]) ** 2 for k in range(3))
            edges.append((dist, i, j))
    edges.sort()

    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            if size[rootX] < size[rootY]:
                rootX, rootY = rootY, rootX
            parent[rootY] = rootX
            size[rootX] += size[rootY]
            return True
        return False

    for dist, u, v in edges:
        if union(u, v):
            if size[find(u)] == n:
                return points[u][0] * points[v][0]

    return -1

with open("part2.txt", "w") as f:
    f.write(str(solve_part2(points)))