ans = 0

with open("input.txt") as f:
    for line in f:
        target, arr = line.split(": ")
        target = int(target)
        arr = list(map(int, arr.split()))

        n = len(arr) - 1
        # Try all possible combinations of + and x on arr
        for i in range(1 << n):
            result = arr[0]
            for j in range(n):
                if i & (1 << j):
                    result += arr[j + 1]
                else:
                    result *= arr[j + 1]
            if result == target:
                ans += target
                break

with open("part1.txt", "w") as f:
    f.write(str(ans))

# Part 2: Either +, x, or || (concatenation)
ans = 0

from tqdm import tqdm

with open("input.txt") as f:
    for line in f:
        target, arr = line.split(": ")
        target = int(target)
        arr = list(map(int, arr.split()))

        n = len(arr) - 1
        # Try all possible combinations of +, x, and || on arr
        for i in range(3 ** n):
            result = arr[0]
            for j in range(n):
                if i % 3 == 0:
                    result += arr[j + 1]
                elif i % 3 == 1:
                    result *= arr[j + 1]
                else:
                    result = int(str(result) + str(arr[j + 1]))
                i //= 3
            if result == target:
                ans += target
                break

with open("part2.txt", "w") as f:
    f.write(str(ans))