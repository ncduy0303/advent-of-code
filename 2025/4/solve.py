from typing import List

# ..@@.@@@@.
# @@@.@.@.@@
# @@@@@.@.@@
# @.@@@@..@.
# @@.@@@@.@@
# .@@@@@@@.@
# .@.@.@.@@@
# @.@@@.@@@@
# .@@@@@@@@.
# @.@.@@@.@.
with open("input.txt") as f:
    # Read input file into grid
    grid = [line.strip() for line in f.readlines()]

# Part 1
# Iterate each cell in grid, and check if there are < 4 @ adjacent among 8 directions
def count_accessible_cells(grid: List[str]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1), (1, 0), (1, 1)]
    accessible_count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '.':
                continue
            adjacent_at = 0
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                    adjacent_at += 1
            if adjacent_at < 4:
                accessible_count += 1
    return accessible_count

with open("part1.txt", "w") as f:
    f.write(str(count_accessible_cells(grid)))

# Part 2
# Remove all accessible cells from grid, then count new accessible cells, repeat until no more can be removed
def count_total_accessible_cells(grid: List[str]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1), (1, 0), (1, 1)]
    total_accessible = 0
    grid_list = [list(row) for row in grid]

    while True:
        to_remove = []
        for r in range(rows):
            for c in range(cols):
                if grid_list[r][c] == '.':
                    continue
                adjacent_at = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid_list[nr][nc] == '@':
                        adjacent_at += 1
                if adjacent_at < 4:
                    to_remove.append((r, c))
        if not to_remove:
            break
        for r, c in to_remove:
            grid_list[r][c] = '.'
        total_accessible += len(to_remove)

    return total_accessible

with open("part2.txt", "w") as f:
    f.write(str(count_total_accessible_cells(grid)))