# .......S.......
# .......|.......
# ......|^|......
# ......|.|......
# .....|^|^|.....
# .....|.|.|.....
# ....|^|^|^|....
# ....|.|.|.|....
# ...|^|^|||^|...
# ...|.|.|||.|...
# ..|^|^|||^|^|..
# ..|.|.|||.|.|..
# .|^|||^||.||^|.
# .|.|||.||.||.|.
# |^|^|^|^|^|||^|
# |.|.|.|.|.|||.|
with open("input.txt") as f:
    # Read the input into a list of strings
    lines = [line.strip() for line in f.readlines()]

# Part 1: Simulate the movement of 'S' and count how many times will the beam be split?
def simulate_movement(lines: list[str]) -> int:
    state: set[int] = set([lines[0].index('S')])
    split_count = 0
    for line in lines[1:]:
        new_state: set[int] = set()
        for pos in state:
            if line[pos] == '.':
                new_state.add(pos)
            elif line[pos] == '^':
                split_count += 1
                if pos > 0:
                    new_state.add(pos - 1)
                if pos < len(line) - 1:
                    new_state.add(pos + 1)
        state = new_state
    return split_count

with open("part1.txt", "w") as f:
    f.write(str(simulate_movement(lines)))

# Part 2: Use DP to count the number of distinct paths from 'S' to the bottom
def count_paths(lines: list[str]) -> int:
    dp: list[int] = [0] * len(lines[0])
    dp[lines[0].index('S')] = 1
    for line in lines[1:]:
        new_dp: list[int] = [0] * len(line)
        for pos in range(len(line)):
            if line[pos] == '.':
                new_dp[pos] = (new_dp[pos] + dp[pos])
            elif line[pos] == '^':
                if pos > 0:
                    new_dp[pos - 1] = (new_dp[pos - 1] + dp[pos])
                if pos < len(line) - 1:
                    new_dp[pos + 1] = (new_dp[pos + 1] + dp[pos])
        dp = new_dp
    return sum(dp)

with open("part2.txt", "w") as f:
    f.write(str(count_paths(lines)))