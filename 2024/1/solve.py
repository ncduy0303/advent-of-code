from collections import Counter

with open("input.txt") as f:
    a, b = map(sorted, zip(*[map(int, line.split()) for line in f.readlines()]))

ans = sum(abs(x - y) for x, y in zip(a, b))

with open("part1.txt", "w") as f:
    f.write(str(ans))

b = Counter(b)
ans = sum(x * b[x] for x in a)

with open("part2.txt", "w") as f:
    f.write(str(ans))