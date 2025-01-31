from collections import deque

with open("input1.txt", "r") as f:
    grid = [list(line.strip()) for line in f]

with open("input2.txt", "r") as f:
    ops = "".join([line.strip() for line in f])

# Find the starting position
for i, row in enumerate(grid):
    for j, cell in enumerate(row):
        if cell == "@":
            x, y = i, j
            break

for op in ops:
    nx, ny = x, y
    if op == "^":
        nx = x - 1
    elif op == "v":
        nx = x + 1
    elif op == "<":
        ny = y - 1
    elif op == ">":
        ny = y + 1

    if grid[nx][ny] == ".":
        grid[x][y] = "."
        grid[nx][ny] = "@"
        x, y = nx, ny
    elif grid[nx][ny] == "O":
        # Push the boxes
        if op == "^":
            while grid[nx][ny] == "O":
                nx -= 1
            if grid[nx][ny] == ".":
                grid[x][y] = "."
                grid[x - 1][y] = "@"
                grid[nx][ny] = "O"
                x, y = x - 1, y
        elif op == "v":
            while grid[nx][ny] == "O":
                nx += 1
            if grid[nx][ny] == ".":
                grid[x][y] = "."
                grid[x + 1][y] = "@"
                grid[nx][ny] = "O"
                x, y = x + 1, y
        elif op == "<":
            while grid[nx][ny] == "O":
                ny -= 1
            if grid[nx][ny] == ".":
                grid[x][y] = "."
                grid[x][y - 1] = "@"
                grid[nx][ny] = "O"
                x, y = x, y - 1
        elif op == ">":
            while grid[nx][ny] == "O":
                ny += 1
            if grid[nx][ny] == ".":
                grid[x][y] = "."
                grid[x][y + 1] = "@"
                grid[nx][ny] = "O"
                x, y = x, y + 1

ans = 0
for x, row in enumerate(grid):
    for y, cell in enumerate(row):
        if cell == "O":
            ans += x * 100 + y

with open("part1.txt", "w") as f:
    f.write(str(ans))

# Part 2: Widen the boxes by 2
def convert(c: str) -> str:
    assert c in ".O@#"
    if c == ".":
        return ".."
    elif c == "O":
        return "[]"
    elif c == "@":
        return "@."
    return "##"

with open("input1.txt", "r") as f:
    grid = [list("".join(map(convert, line.strip()))) for line in f]

# Find the starting position
for i, row in enumerate(grid):
    for j, cell in enumerate(row):
        if cell == "@":
            x, y = i, j
            break

for op in ops:
    nx, ny = x, y
    if op == "^":
        nx = x - 1
    elif op == "v":
        nx = x + 1
    elif op == "<":
        ny = y - 1
    elif op == ">":
        ny = y + 1

    if grid[nx][ny] == ".":
        grid[x][y] = "."
        grid[nx][ny] = "@"
        x, y = nx, ny
    elif grid[nx][ny] == "[":
        assert op in "^v>" and grid[nx][ny + 1] == "]"
        if op == "^":
            blocks = [[(nx, ny)]]
            pushable = True
            expand = True
            while pushable and expand:
                expand = False
                block = []
                for cell in blocks[-1]:
                    if grid[cell[0] - 1][cell[1]] == "[":
                        assert grid[cell[0] - 1][cell[1] + 1] == "]"
                        block.append((cell[0] - 1, cell[1]))
                        expand = True
                    if grid[cell[0] - 1][cell[1] - 1] == "[":
                        assert grid[cell[0] - 1][cell[1]] == "]"
                        block.append((cell[0] - 1, cell[1] - 1))
                        expand = True
                    if grid[cell[0] - 1][cell[1] + 1] == "[":
                        assert grid[cell[0] - 1][cell[1] + 2] == "]"
                        block.append((cell[0] - 1, cell[1] + 1))
                        expand = True
                    if grid[cell[0] - 1][cell[1]] == "#" or grid[cell[0] - 1][cell[1] + 1] == "#":
                        pushable = False
                        break
                if expand:
                    block = list(set(block))
                    blocks.append(block)
            if pushable:
                for block in blocks[::-1]:
                    for cell in block:
                        assert grid[cell[0] - 1][cell[1]] == "." and grid[cell[0] - 1][cell[1] + 1] == "."
                        grid[cell[0] - 1][cell[1]] = "["
                        grid[cell[0] - 1][cell[1] + 1] = "]"
                        grid[cell[0]][cell[1]] = "."
                        grid[cell[0]][cell[1] + 1] = "."
                grid[nx][ny] = "@"
                grid[x][y] = "."
                x, y = nx, ny
        elif op == "v":
            blocks = [[(nx, ny)]]
            pushable = True
            expand = True
            while pushable and expand:
                expand = False
                block = []
                for cell in blocks[-1]:
                    if grid[cell[0] + 1][cell[1]] == "[":
                        assert grid[cell[0] + 1][cell[1] + 1] == "]"
                        block.append((cell[0] + 1, cell[1]))
                        expand = True
                    if grid[cell[0] + 1][cell[1] - 1] == "[":
                        assert grid[cell[0] + 1][cell[1]] == "]"
                        block.append((cell[0] + 1, cell[1] - 1))
                        expand = True
                    if grid[cell[0] + 1][cell[1] + 1] == "[":
                        assert grid[cell[0] + 1][cell[1] + 2] == "]"
                        block.append((cell[0] + 1, cell[1] + 1))
                        expand = True
                    if grid[cell[0] + 1][cell[1]] == "#" or grid[cell[0] + 1][cell[1] + 1] == "#":
                        pushable = False
                        break
                if expand:
                    block = list(set(block))
                    blocks.append(block)
            if pushable:
                for block in blocks[::-1]:
                    for cell in block:
                        assert grid[cell[0] + 1][cell[1]] == "." and grid[cell[0] + 1][cell[1] + 1] == "."
                        grid[cell[0] + 1][cell[1]] = "["
                        grid[cell[0] + 1][cell[1] + 1] = "]"
                        grid[cell[0]][cell[1]] = "."
                        grid[cell[0]][cell[1] + 1] = "."
                grid[nx][ny] = "@"
                grid[x][y] = "."
                x, y = nx, ny
        elif op == ">":
            while grid[nx][ny] in "[]":
                ny += 1
            if grid[nx][ny] == ".":
                grid[nx][ny] = "]"
                for i in range(ny - 1, y, -1):
                    grid[nx][i] = grid[nx][i - 1]
                grid[x][y] = "."
                grid[x][y + 1] = "@"
                x, y = x, y + 1
    elif grid[nx][ny] == "]":
        assert op in "^v<" and grid[nx][ny - 1] == "["
        if op == "^":
            blocks = [[(nx, ny)]]
            pushable = True
            expand = True
            while pushable and expand:
                expand = False
                block = []
                for cell in blocks[-1]:
                    if grid[cell[0] - 1][cell[1]] == "]":
                        assert grid[cell[0] - 1][cell[1] - 1] == "["
                        block.append((cell[0] - 1, cell[1]))
                        expand = True
                    if grid[cell[0] - 1][cell[1] + 1] == "]":
                        assert grid[cell[0] - 1][cell[1]] == "["
                        block.append((cell[0] - 1, cell[1] + 1))
                        expand = True
                    if grid[cell[0] - 1][cell[1] - 1] == "]":
                        assert grid[cell[0] - 1][cell[1] - 2] == "["
                        block.append((cell[0] - 1, cell[1] - 1))
                        expand = True
                    if grid[cell[0] - 1][cell[1]] == "#" or grid[cell[0] - 1][cell[1] - 1] == "#":
                        pushable = False
                        break
                if expand:
                    block = list(set(block))
                    blocks.append(block)
            if pushable:
                for block in blocks[::-1]:
                    for cell in block:
                        assert grid[cell[0] - 1][cell[1]] == "." and grid[cell[0] - 1][cell[1] - 1] == "."
                        grid[cell[0] - 1][cell[1]] = "]"
                        grid[cell[0] - 1][cell[1] - 1] = "["
                        grid[cell[0]][cell[1]] = "."
                        grid[cell[0]][cell[1] - 1] = "."
                grid[nx][ny] = "@"
                grid[x][y] = "."
                x, y = nx, ny
        elif op == "v":
            blocks = [[(nx, ny)]]
            pushable = True
            expand = True
            while pushable and expand:
                expand = False
                block = []
                for cell in blocks[-1]:
                    if grid[cell[0] + 1][cell[1]] == "]":
                        assert grid[cell[0] + 1][cell[1] - 1] == "["
                        block.append((cell[0] + 1, cell[1]))
                        expand = True
                    if grid[cell[0] + 1][cell[1] + 1] == "]":
                        assert grid[cell[0] + 1][cell[1]] == "["
                        block.append((cell[0] + 1, cell[1] + 1))
                        expand = True
                    if grid[cell[0] + 1][cell[1] - 1] == "]":
                        assert grid[cell[0] + 1][cell[1] - 2] == "["
                        block.append((cell[0] + 1, cell[1] - 1))
                        expand = True
                    if grid[cell[0] + 1][cell[1]] == "#" or grid[cell[0] + 1][cell[1] - 1] == "#":
                        pushable = False
                        break
                if expand:
                    block = list(set(block))
                    blocks.append(block)
            if pushable:
                for block in blocks[::-1]:
                    for cell in block:
                        assert grid[cell[0] + 1][cell[1]] == "." and grid[cell[0] + 1][cell[1] - 1] == "."
                        grid[cell[0] + 1][cell[1]] = "]"
                        grid[cell[0] + 1][cell[1] - 1] = "["
                        grid[cell[0]][cell[1]] = "."
                        grid[cell[0]][cell[1] - 1] = "."
                grid[nx][ny] = "@"
                grid[x][y] = "."
                x, y = nx, ny
        elif op == "<":
            while grid[nx][ny] in "[]":
                ny -= 1
            if grid[nx][ny] == ".":
                grid[nx][ny] = "["
                for i in range(ny + 1, y):
                    grid[nx][i] = grid[nx][i + 1]
                grid[x][y] = "."
                grid[x][y - 1] = "@"
                x, y = x, y - 1
    
    # print(f"Operation: {op}")
    # for row in grid:
    #     print("".join(row))
    # print()

ans = 0
for x, row in enumerate(grid):
    for y, cell in enumerate(row):
        if cell == "[":
            ans += x * 100 + y

with open("part2.txt", "w") as f:
    f.write(str(ans))