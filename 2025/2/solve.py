# 82853534-82916516,2551046-2603239,805115-902166,3643-7668,4444323719-4444553231,704059-804093,32055-104187,7767164-7799624,25-61,636-1297,419403897-419438690,66-143,152-241,965984-1044801,1-19,376884-573880,9440956-9477161,607805-671086,255-572,3526071225-3526194326,39361322-39455443,63281363-63350881,187662-239652,240754-342269,9371-26138,1720-2729,922545-957329,3477773-3688087,104549-119841
with open("input.txt") as f:
    # Read input file into [(l1, r1), (l2, r2), ...]
    ranges = [tuple(map(int, part.split("-"))) for part in f.read().strip().split(",")]

# Part 1
# Iterate through each number in each range, and check if it is invalid
def is_invalid(num: int) -> bool:
    s = str(num)
    n = len(s)
    if n % 2 != 0:
        return False
    return s[: n // 2] == s[n // 2 :]

res = 0
for l, r in ranges:
    for num in range(l, r + 1):
        if is_invalid(num):
            res += num

with open("part1.txt", "w") as f:
    f.write(str(res))

# Part 2
# Same as part 1, but the invalid condition is different
def is_invalid_2(num: int) -> bool:
    s = str(num)
    n = len(s)
    # Check all divisors of n
    for d in range(1, n // 2 + 1):
        if n % d == 0:
            if all(s[i] == s[i + d] for i in range(n - d)) and n // d >= 2:
                return True
    return False

res = 0
for l, r in ranges:
    for num in range(l, r + 1):
        if is_invalid_2(num):
            res += num

with open("part2.txt", "w") as f:
    f.write(str(res))