import re

ans = 0

# Match all "mul(X,Y)", where X and Y are each 1-3 digit numbers using regex
with open("input.txt", "r") as f:
    for line in f:
        for m in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)", line):
            ans += int(m.group(1)) * int(m.group(2))

with open("part1.txt", "w") as f:
    f.write(str(ans))

ans = 0
enable = True

# Now need to match "do()" and "don't()" to enable/disable the multiplication
with open("input.txt", "r") as f:
    for line in f:
        for m in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)", line):
            if m.group(0) == "do()":
                enable = True
            elif m.group(0) == "don't()":
                enable = False
            else:
                if enable: 
                    ans += int(m.group(1)) * int(m.group(2))

with open("part2.txt", "w") as f:
    f.write(str(ans))