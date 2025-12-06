from typing import List

# 123 328  51 64 
#  45 64  387 23 
#   6 98  215 314
# *   +   *   +  
with open("input.txt") as f:
    # Read and parse the input file into a matrix of integers, with the last line as operators
    lines = f.readlines()
    matrix: List[List[int]] = [list(map(int, line.split())) for line in lines[:-1]]
    operators: List[str] = lines[-1].split()

# Part 1: Calculate the result of applying the operators to each column, and sum the results
def apply_operator(a: int, b: int, operator: str) -> int:
    if operator == '+':
        return a + b
    elif operator == '*':
        return a * b
    else:
        raise ValueError(f"Unknown operator: {operator}")
    
def calculate_column_results(matrix: List[List[int]], operators: List[str]) -> int:
    total = 0
    for col in range(len(matrix[0])):
        col_values = [matrix[row][col] for row in range(len(matrix))]
        result = col_values[0]
        for row in range(1, len(col_values)):
            result = apply_operator(result, col_values[row], operators[col])
        total += result
    return total

with open("part1.txt", "w") as f:
    f.write(str(calculate_column_results(matrix, operators)))

# Part 2: Reading the problems right-to-left one column at a time, the problems are now quite different:
# The rightmost problem is 4 + 431 + 623 = 1058
# The second problem from the right is 175 * 581 * 32 = 3253600
# The third problem from the right is 8 + 248 + 369 = 625
# Finally, the leftmost problem is 356 * 24 * 1 = 8544
# Now, the grand total is 1058 + 3253600 + 625 + 8544 = 3263827.

# Need to align the numbers as we read them
with open("input.txt") as f:
    lines = f.readlines()
    matrix_str: List[str] = [line.rstrip("\n") for line in lines[:-1]]
    operators_str: str = lines[-1].rstrip("\n")

def calculate_aligned_column_results(matrix_str: List[str], operators_str: str) -> int:
    total = 0
    idx = 0
    cur = 0
    operator = None
    while idx < len(operators_str):
        if operators_str[idx] != ' ':
            total += cur
            operator = operators_str[idx]
            cur = 0 if operator == '+' else 1
        num = None
        for row in matrix_str:
            if row[idx] == ' ':
                continue
            digit = int(row[idx])
            num = num * 10 + digit if num is not None else digit
        assert operator is not None
        if num is not None:
            cur = apply_operator(cur, num, operator)
        idx += 1
    total += cur
    return total

with open("part2.txt", "w") as f:
    f.write(str(calculate_aligned_column_results(matrix_str, operators_str)))