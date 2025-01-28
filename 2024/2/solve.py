from typing import List

# Check if the list satisfy the constraint:
def check(a: List[int]) -> bool:
    # The levels are either all increasing or all decreasing.
    # Any two adjacent levels differ by at least one and at most three.
    for i in range(1, len(a)):
        if (a[i] - a[i - 1]) * (a[1] - a[0]) <= 0:
            return False
        if abs(a[i] - a[i - 1]) > 3 or abs(a[i] - a[i - 1]) < 1:
            return False
    return True

with open("input.txt", "r") as f:
    all_lists = [list(map(int, line.split())) for line in f.readlines()]

ans = sum(check(a) for a in all_lists)

with open("part1.txt", "w") as f:
    f.write(str(ans))

# Check if the list satisfy the constraint if we can remove at most one element
# Can just brute force as input size is small
def check2(a: List[int]) -> int:
    # The levels are either all increasing or all decreasing.
    # Any two adjacent levels differ by at least one and at most three.
    ok = False
    for i in range(len(a)):
        ok |= check(a[:i] + a[i + 1:])
    return ok

ans = sum(check2(a) for a in all_lists)

with open("part2.txt", "w") as f:
    f.write(str(ans))