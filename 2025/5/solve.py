from typing import List, Tuple

# 3-5
# 10-14
# 16-20
# 12-18
# (empty line)
# 1
# 5
# 8
# 11
# 17
# 32

# Read the fresh ingredient ranges, and the list of available ingredients from the input file
with open("input.txt") as f:
    fresh_ingredient_ranges = [(int(parts[0]), int(parts[1])) for line in f.readlines() if "-" in line for parts in [line.strip().split("-")]]
with open("input.txt") as f:
    available_ingredients = [int(line.strip()) for line in f.readlines() if line.strip().isdigit()]

# Part 1: Count how many available ingredients are fresh
# Check if the ingredient falls within any of the fresh ingredient ranges
def is_fresh(ingredient: int, fresh_ranges: List[Tuple[int, int]]) -> bool:
    for start, end in fresh_ranges:
        if start <= ingredient <= end:
            return True
    return False

fresh_count = sum(1 for ingredient in available_ingredients if is_fresh(ingredient, fresh_ingredient_ranges))
with open("part1.txt", "w") as f:
    f.write(str(fresh_count))

# Part 2: Count how many ingredients are considered fresh

def count_fresh_ingredients(fresh_ranges: List[Tuple[int, int]]) -> int:
    fresh_ranges.sort()
    total_fresh = 0
    current_start, current_end = fresh_ranges[0]
    for start, end in fresh_ranges[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            total_fresh += current_end - current_start + 1
            current_start, current_end = start, end
    total_fresh += current_end - current_start + 1
    return total_fresh

with open("part2.txt", "w") as f:
    f.write(str(count_fresh_ingredients(fresh_ingredient_ranges)))