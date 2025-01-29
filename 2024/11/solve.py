from functools import cache

with open("input.txt") as f:
    arr = list(map(int, f.readline().split()))

# Simulate the process 25 times
for _ in range(25):
    new_arr = []
    for x in arr:
        if x == 0:
            new_arr.append(1)
        elif len(str(x)) % 2 == 0:
            new_arr.append(int(str(x)[:len(str(x))//2]))
            new_arr.append(int(str(x)[len(str(x))//2:]))
        else:
            new_arr.append(x * 2024)
    arr = new_arr

ans = len(arr)

with open("part1.txt", "w") as f:
    f.write(str(ans))

# Part 2: Simulate the process 75 times
# 2^75 is too large to simulate, do memoization instead

@cache
def solve(x: int, k: int) -> int:
    if k == 0:
        return 1
    if x == 0:
        return solve(1, k-1)
    if len(str(x)) % 2 == 0:
        return solve(int(str(x)[:len(str(x))//2]), k-1) + solve(int(str(x)[len(str(x))//2:]), k-1)
    return solve(x * 2024, k-1)

with open("input.txt") as f:
    arr = list(map(int, f.readline().split()))

ans = sum(solve(x, 75) for x in arr)

with open("part2.txt", "w") as f:
    f.write(str(ans))