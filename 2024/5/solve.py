from typing import List
from collections import deque

with open("input1.txt") as f:
    # (i, j) means page i must be before page j
    rules = set(tuple(map(int, line.split("|"))) for line in f)

with open("input2.txt") as f:
    updates = [list(map(int, line.split(","))) for line in f]

# Check if the page order in the update is valid
def check(update: List[int]) -> bool:
    assert len(update) % 2 == 1 # Must be odd
    for i in range(len(update) - 1):
        for j in range(i + 1, len(update)):
            if (update[j], update[i]) in rules:
                return False
    return True

# Sum the middle number of each update if the update is valid
ans = sum(update[len(update) // 2] for update in updates if check(update))

with open("part1.txt", "w") as f:
    f.write(str(ans))

# Part 2: Fix the invalid updates
# Do a topological sort to find the correct order for each update
def topological_sort(graph: List[List[int]]) -> List[int]:
    n = len(graph)
    in_degree = [0] * n
    for i in range(n):
        for j in graph[i]:
            in_degree[j] += 1
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order = []
    while queue:
        i = queue.popleft()
        order.append(i)
        for j in graph[i]:
            in_degree[j] -= 1
            if in_degree[j] == 0:
                queue.append(j)
    return order

ans = 0

for update in updates:
    if not check(update):
        graph = [[] for _ in range(len(update))]
        for i in range(len(update) - 1):
            for j in range(i + 1, len(update)):
                if (update[i], update[j]) in rules:
                    graph[i].append(j)
                elif (update[j], update[i]) in rules:
                    graph[j].append(i)
        order = topological_sort(graph)
        update[:] = [update[i] for i in order]
        ans += update[len(update) // 2]

with open("part2.txt", "w") as f:
    f.write(str(ans))