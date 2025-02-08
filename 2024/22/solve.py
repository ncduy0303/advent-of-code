from collections import defaultdict

with open("input.txt", "r") as f:
    arr = list(map(int, f.read().split()))

def op(x: int) -> int:
    x = (x ^ (x << 6)) & ((1 << 24) - 1)
    x = (x ^ (x >> 5)) & ((1 << 24) - 1)
    x = (x ^ (x << 11)) & ((1 << 24) - 1)
    return x

ans = 0
for x in arr:
    for _ in range(2000):
        x = op(x)
    ans += x

with open("part1.txt", "w") as f:
    f.write(str(ans))

# Part 2: Find the best 4 numbers tuple of consecutive changes that will maximise the sum

seqs = []
for x in arr:
    seq = [x % 10]
    for _ in range(2000):
        x = op(x)
        seq.append(x % 10)
    seqs.append(seq)

tuple2sum = defaultdict(int)
for seq in seqs:
    tuple2val = {}
    for i in range(1, len(seq) - 3):
        tup = (seq[i] - seq[i - 1], seq[i + 1] - seq[i], seq[i + 2] - seq[i + 1], seq[i + 3] - seq[i + 2])
        if tup not in tuple2val:
            tuple2val[tup] = seq[i + 3]
    for tup, val in tuple2val.items():
        tuple2sum[tup] += val

ans = max(tuple2sum.values())
with open("part2.txt", "w") as f:
    f.write(str(ans))