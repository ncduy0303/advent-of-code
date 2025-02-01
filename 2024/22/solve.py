with open("input.txt", "r") as f:
    arr = list(map(int, f.read().split()))

def f(x: int) -> int:
    x = (x ^ (x << 6)) & ((1 << 24) - 1)
    x = (x ^ (x >> 5)) & ((1 << 24) - 1)
    x = (x ^ (x << 11)) & ((1 << 24) - 1)
    return x

ans = 0
for x in arr:
    for _ in range(2000):
        x = f(x)
    ans += x

with open("part1.txt", "w") as f:
    f.write(str(ans))