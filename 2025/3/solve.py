# 987654321111111
# 811111111111119
# 234234234234278
# 818181911112111
# ... (more lines) ...
with open("input.txt") as f:
    # Read input file into [s1, s2, ...]
    banks = [line.strip() for line in f.readlines()]

# Part 1
# Iterate through each number in each range, and check if it is invalid
def get_max_value(bank: str) -> int:
    """Get the maximum value from any 2 digits (same order) in the bank string."""
    max_value = -1
    for i in range(len(bank)):
        for j in range(i + 1, len(bank)):
            value = int(bank[i]) * 10 + int(bank[j])
            if value > max_value:
                max_value = value
    return max_value

res = sum(get_max_value(bank) for bank in banks)
with open("part1.txt", "w") as f:
    f.write(str(res))

# Part 2
def get_max_value_2(bank: str) -> int:
    """Get the maximum value from any 12 digits (same order) in the bank string."""
    n = len(bank)
    m = 12
    # dp = [[-1] * (m + 1) for _ in range(n + 1)]
    # for i in range(n + 1):
    #     dp[i][0] = 0
    # for i in range(1, n + 1):
    #     for j in range(1, min(i, m) + 1):
    #         dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - 1] * 10 + int(bank[i - 1]))
    # return dp[n][m]

    # Use a more space-efficient approach
    dp = [-1] * (m + 1)
    dp[0] = 0
    for i in range(1, n + 1):
        for j in range(min(i, m), 0, -1):
            dp[j] = max(dp[j], dp[j - 1] * 10 + int(bank[i - 1]))
    return dp[m]

res = sum(get_max_value_2(bank) for bank in banks)
with open("part2.txt", "w") as f:
    f.write(str(res))