with open("input.txt", "r") as f:
    edges = [line.strip().split("-") for line in f]

str2idx = {}
idx2str = []
for u, v in edges:
    if u not in str2idx:
        str2idx[u] = len(str2idx)
        idx2str.append(u)
    if v not in str2idx:
        str2idx[v] = len(str2idx)
        idx2str.append(v)
n = len(str2idx)
adj = [[False] * n for _ in range(n)]
for u, v in edges:
    u, v = str2idx[u], str2idx[v]
    adj[u][v] = adj[v][u] = True
ans = 0
for i in range(n):
    for j in range(i + 1, n):
        for k in range(j + 1, n):
            if adj[i][j] and adj[j][k] and adj[k][i] and (idx2str[i].startswith("t") or idx2str[j].startswith("t") or idx2str[k].startswith("t")):
                ans += 1

with open("part1.txt", "w") as f:
    f.write(str(ans))

# Part 2: Find the largest clique in the graph
# Use https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
adj = [[] for _ in range(n)]
for u, v in edges:
    u, v = str2idx[u], str2idx[v]
    adj[u].append(v)
    adj[v].append(u)

def bron_kerbosch(R, P, X, graph):
    if not P and not X:
        yield R
    while P:
        v = P.pop()
        yield from bron_kerbosch(
            R.union({v}),
            P.intersection(graph[v]),
            X.intersection(graph[v]),
            graph
        )
        X.add(v)

graph = [set(neighbors) for neighbors in adj]
all_cliques = list(bron_kerbosch(set(), set(range(n)), set(), graph))
largest_clique = max(all_cliques, key=len)
ans = ",".join(sorted(list(map(lambda i: idx2str[i], largest_clique))))

with open("part2.txt", "w") as f:
    f.write(ans)