with open("input.txt") as f:
    # Read rotation instructions into [(direction, steps), ...]
    rots = [(line[0], int(line[1:])) for line in f.readlines()]

# Part 1
# Simulate a circle of [0, 99]
# Count number of times it visits 0 at the end
cur = 50
res = 0
for d, s in rots:
    if d == "R":
        cur = (cur + s) % 100
    else:
        cur = (cur - s) % 100
    if cur == 0:
        res += 1

with open("part1.txt", "w") as f:
    f.write(str(res))

# Part 2
# Count number of times it passes 0 during movement
# Note: 1 rotation may pass 0 multiple times
cur = 50
res = 0
for d, s in rots:
    if d == "R":
        res += (cur + s) // 100
        cur = (cur + s) % 100
    else:
        # 0 -> 1 (if we start at 0, we don't count this)
        # -100 -> 2
        # -101 -> 2
        # -200 -> 3
        res += -(cur - s) // 100 + 1
        if cur == 0:
            res -= 1
        cur = (cur - s) % 100

with open("part2.txt", "w") as f:
    f.write(str(res))