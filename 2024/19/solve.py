from functools import cache

with open("input1.txt", "r") as f:
    arr = f.read().split(", ")

with open("input2.txt", "r") as f:
    queries = f.read().splitlines()

ans = 0
for query in queries:
    # Check if the query can be constructed from an unlimited combination of the elements in the array
    @cache
    def solve(s: str) -> bool:
        if not s:
            return True
        for p in arr:
            if s.startswith(p) and solve(s[len(p):]):
                return True
        return False

    if solve(query):
        ans += 1

with open("part1.txt", "w") as f:
    f.write(str(ans))

ans = 0
for query in queries:
    # Count the number of ways that the query can be constructed from an unlimited combination of the elements in the array
    @cache
    def solve(s: str) -> int:
        if not s:
            return 1
        res = 0
        for p in arr:
            if s.startswith(p):
                res += solve(s[len(p):])
        return res

    ans += solve(query)

with open("part2.txt", "w") as f:
    f.write(str(ans))